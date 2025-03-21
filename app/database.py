import sqlite3

def get_db_connection():
    """Connexion à la base de données SQLite.
    """
    conn = sqlite3.connect("athlete_performance.db")
    conn.row_factory = sqlite3.Row  # Permet d'accéder aux colonnes par leur nom
    return conn

def create_tables():
    """Création des tables de la base de données SQLite.
    """
    conn = get_db_connection()
    cursor = conn.cursor()
    
   # Table des utilisateurs (user)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id_user INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL UNIQUE,
        nom TEXT NOT NULL,
        prenom TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        token TEXT,
        password TEXT NOT NULL,
        role TEXT CHECK(role IN ('coach', 'athlete')) NOT NULL
    )
    ''')

    # Table des détails de l'utilisateur (details)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS details (
        id_details INTEGER PRIMARY KEY AUTOINCREMENT,
        id_user INTEGER NOT NULL,
        gender TEXT,
        age INTEGER,
        weight REAL,
        height REAL,
        FOREIGN KEY (id_user) REFERENCES users(id_user)
    )
    ''')

    # Table des performances (performance)
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS performances (
        id_performance INTEGER PRIMARY KEY AUTOINCREMENT,
        id_user INTEGER NOT NULL,
        power_max REAL,
        hr_max REAL,
        vo2_max REAL,
        rf_max REAL,
        cadence_max REAL,
        vo2_class TEXT,
        ressenti INTEGER,
        date_performance TEXT DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (id_user) REFERENCES users(id_user)
    )
    ''')

    conn.commit()
    conn.close()

# Création des tables au lancement du script
create_tables()