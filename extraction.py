from datetime import datetime
import json
import re
import sqlite3
import os
from rich import print  # Pour un affichage coloré (optionnel)

# 🔹 Chemin de ta base SQLite
DB_PATH = "athlete_performance.db"

# 🔹 Dossier où se trouvent les fichiers JSON
JSON_DIR = "app\\utils\\data"

# 🔹 Connexion à la base SQLite
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

# 🔹 Création de la table si elle n'existe pas
cursor.execute("""
CREATE TABLE IF NOT EXISTS performances (
    id_performance INTEGER PRIMARY KEY AUTOINCREMENT,
    id_user INTEGER NOT NULL,
    power_max REAL,
    hr_max REAL,
    vo2_max REAL,
    rf_max REAL,
    cadence_max REAL,
    vo2_class TEXT,
    ressenti INTEGER DEFAULT NULL,
    date_performance TEXT DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (id_user) REFERENCES users(id_user)
);
""")
conn.commit()

# 🔹 Fonction pour insérer les données
def insert_performance(data, id_user):
    """ Insère une performance dans la base de données avec id_user extrait du nom du fichier """
    date_performance = datetime.now().strftime('%Y-%m-%d %H:%M:%S')  # Date actuelle
    ressenti = data.get("ressenti", 5)  # Valeur par défaut : 5

    # Extraction des valeurs depuis le JSON
    power_max = data.get("power.max", None)
    hr_max = data.get("hr.max", None)
    vo2_max = data.get("vo2.max", None)
    rf_max = data.get("rf.max", None)
    cadence_max = data.get("cadence.max", None)
    vo2_class = json.dumps(data.get("vo2.class", []))  # Stocke comme JSON, [74, 88] dans cet exemple

    # Affiche les données pour débogage
    print(f"🎯 Données à insérer pour ID utilisateur {id_user}:")
    print(f"Power Max: {power_max}, HR Max: {hr_max}, VO2 Max: {vo2_max}, RF Max: {rf_max}, Cadence Max: {cadence_max}, VO2 Class: {vo2_class}, Ressenti: {ressenti}, Date Performance: {date_performance}")

    cursor.execute("""
    INSERT INTO performances (id_user, power_max, hr_max, vo2_max, rf_max, cadence_max, vo2_class, ressenti, date_performance)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        id_user,
        power_max,
        hr_max,
        vo2_max,
        rf_max,
        cadence_max,
        vo2_class,
        ressenti,
        date_performance
    ))
    conn.commit()
    print(f"[bold green]✅ Performance insérée pour ID utilisateur {id_user}[/bold green]")

# 🔹 Lire et traiter les fichiers JSON
def load_json_files():
    """ Charge les fichiers JSON et insère les performances """
    for file_name in os.listdir(JSON_DIR):
        match = re.match(r"sbj_(\d+)\.json", file_name)  # Extrait N depuis "sbj_N.json"
        if match:
            id_user = int(match.group(1))  # Convertit N en entier
            file_path = os.path.join(JSON_DIR, file_name)
            print(f"[bold cyan]📂 Chargement : {file_name} | ID utilisateur : {id_user}[/bold cyan]")

            with open(file_path, "r", encoding="utf-8") as f:
                try:
                    json_data = json.load(f)

                    # Si le JSON est un objet unique, le convertir en liste
                    if isinstance(json_data, dict):
                        json_data = [json_data]

                    for entry in json_data:
                        insert_performance(entry, id_user)
                except json.JSONDecodeError as e:
                    print(f"[bold red]❌ Erreur JSON dans {file_name} : {e}[/bold red]")
        else:
            print(f"[bold yellow]⚠️ Fichier ignoré : {file_name} (nom incorrect)[/bold yellow]")

# 🔹 Exécuter le script
if __name__ == "__main__":
    try:
        load_json_files()
    finally:
        conn.close()
        print("[bold magenta]🚀 Chargement terminé ![/bold magenta]")