from flask import Flask, jsonify, request, render_template, redirect, session, flash, url_for
from flask_cors import CORS # importerer cors for å tillate kobling fra andre domener 
from dotenv import load_dotenv # importerer dotenv for å lese det som står i .env filen og for å gjøre det tigjengelig i Python
import os # importeres for å hente ting skrevet i .env filen
import mariadb # importeres for å kunne snakke med DB
import mariadb # importeres for å kunne snakke med DB

load_dotenv()

app = Flask(__name__)
app.secret_key = 'endre-meg-til-noe-hemmelig'
CORS(app)

def db_connection(): # funskjonen for å koble til DB
        return mariadb.connect( # kobler på DB ved å bruke .env info 
           host=os.getenv('DB_HOST'), # host 
           user=os.getenv('DB_USER'), # bruker
           password=os.getenv('DB_PASS'), # passord
           database=os.getenv('DB_NAME') # database navn
        )
        
@app.route('/') # hovedsiden
def index(): 
    return render_template('register.html') # returnerer register siden


@app.route('/submit', methods = ['POST']) # route for å sende inn registrerings skjema
def submit():
   
    if request.method == 'POST': # sjekker om metoden er POST
        Brukernavn = request.form['fullt_navn'] # henter data fra skjemaet ved hjelp av navn
        epost = request.form['epost'] # 
        passord = request.form['passord']
                
        connect = db_connection() # kobler til DB 
        cursor = connect.cursor() # lager en cursor for å utføre SQL spørringer
        
        cursor.execute( 
            'INSERT INTO brukere(Brukernavn, Epost, Passord) VALUES(?, ?, ?)', # setter inn data i brukere tabellen
             (Brukernavn, epost, passord) 
        )
        
        connect.commit() # lagrer endringene i DB
        cursor.close() # lukker cursor
        
        return redirect('/login') # etter registrering, redirecter til login siden
    
    return render_template('register.html') 



@app.route('/login', methods = ['GET','POST'])  # route for login siden
def login():
    if request.method == 'POST': 
        epost = request.form['epost']
        passord = request.form['passord']
        
        connect = db_connection() #
        cursor = connect.cursor()
        
        cursor.execute('SELECT * FROM brukere WHERE epost = %s AND passord = %s', (epost, passord)) # sjekker om epost og passord matcher en bruker i DB
        user = cursor.fetchone() # henter den første raden som matcher
         
        cursor.close()
        connect.close()
        
        if user: # hvis en bruker ble funnet
            session['brukere_id'] = user[0] # lagrer bruker ID i session
            session['brukernavn'] = user[1] # lagrer brukernavn i session
            return redirect('/tickets') # redirecter til tickets siden
        else:
            flash('Feil epost eller passord!') 
            return redirect('/login')
    
    return render_template('login.html') 

    
@app.route('/tickets')
def tickets():
    if 'brukere_id' not in session: # sjekker om bruker er logget inn
        return redirect('/login') 
    
    user_id = session['brukere_id'] # henter bruker ID fra session
    
    connect = db_connection()
    cursor = connect.cursor()
    cursor.execute('SELECT * FROM tickets WHERE user_id = %s ORDER BY Id DESC', (user_id,)) # henter alle tickets for den innloggede brukeren
    alle_tickets = cursor.fetchall() # henter alle radene
    cursor.close()
    connect.close()

    return render_template('tickets.html', brukernavn=session.get('brukernavn'), tickets=alle_tickets) # returnerer tickets siden med brukernavn og tickets data



@app.route('/opprett_ticket', methods=['POST']) # route for å opprette en ny ticket
def opprett_ticket():
    if 'brukere_id' not in session:
        return redirect('/login')
    
    Overskrift = request.form['overskrift']
    Beksrivelse = request.form['beskrivelse']
    Kategori = request.form['kategori']
    Statusen = request.form['status']
    user_id = int(session['brukere_id']) # henter bruker ID fra session
    
    connect = db_connection()
    cursor = connect.cursor()
    
    cursor.execute(
        'INSERT INTO tickets(Overskrift, Beksrivelse, Kategori, Statusen, user_id) VALUES(%s, %s, %s, %s, %s)', # setter inn ny ticket i tickets tabellen
        (Overskrift, Beksrivelse, Kategori, Statusen, user_id)
    )
    
    connect.commit()
    cursor.close()
    connect.close()
    
    return redirect('/tickets')
 
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)