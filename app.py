from flask import Flask, jsonify, request 
from flask_cors import CORS # importerer cors for å tillate kobling fra andre domener 
from dotenv import load_dotenv # importerer dotenv for å lese det som står i .env filen og for å gjøre det tigjengelig i Python
import os # importeres for å hente ting skrevet i .env filen
import requests # dette importeres for at API-kall skal fungere
import mariadb # importeres for å kunne snakke med DB
import mariadb # iporteres for å kunne snakke med DB

load_dotenv()

app = Flask(__name__)
CORS(app)











 
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3000, debug=True)