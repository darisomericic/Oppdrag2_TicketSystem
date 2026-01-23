create table brukere (
    Id SERIAL PRIMARY KEY,
    Brukernavn VARCHAR(255) NOT NULL,
    Epost VARCHAR(255) NOT NULL,
    Passord VARCHAR(255) NOT NULL,
    Rolle VARCHAR(20) NOT NULL DEFAULT 'bruker'
);

create table tickets (
    Id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    user_id BIGINT UNSIGNED NOT NULL,
    Overskrift VARCHAR(100) NOT NULL,
    Beskrivelse TEXT NOT NULL,
    Kategori VARCHAR(255) NOT NULL, 
    Statusen VARCHAR(20) NOT NULL DEFAULT 'åpen',
    handler_id BIGINT UNSIGNED, 
    FOREIGN KEY (user_id) REFERENCES brukere(id),     
    FOREIGN KEY (handler_id) REFERENCES brukere(id)
);