# -> Importation de la librairie sqlite3
import sqlite3

# -> Connexion à la base de données SQLite
db_connexion = sqlite3.connect("sqlalchemy_training.db")
db_curseur = db_connexion.cursor()

# -> Création de la table "phones" (si elle n'existe pas déjà)
db_curseur.execute("""
CREATE TABLE IF NOT EXISTS phones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    marque TEXT NOT NULL,
    modele TEXT NOT NULL,
    prix INTEGER NOT NULL
)
""")

db_curseur.execute("""
CREATE TABLE IF NOT EXISTS utilisateurs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nom TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE
)
""")

# -> Insertion de données dans la table "phones"
db_curseur.execute("""
INSERT INTO phones (marque, modele, prix)
VALUES (?, ?, ?)
""", ("Samsung", "Galaxy A55", 449))

db_curseur.execute("""
INSERT INTO phones (marque, modele, prix)
VALUES (?, ?, ?)
""", ("Samsung", "Galaxy Z Flip6", 1199))

db_curseur.execute("""
SELECT id, marque, modele, prix
FROM phones
WHERE prix > ?
ORDER BY prix DESC
LIMIT 1
""", (800,))

db_telephones = db_curseur.fetchall()

for query_telephones in db_telephones:
    id_telephone, marque, modele, prix = query_telephones
    print(f"ID: {id_telephone} • Le téléphone \"{marque} {modele}\" coûte {prix}€")

# -> Insertion de données dans la table "utilisateurs"
db_curseur.execute("""
INSERT OR IGNORE INTO utilisateurs (nom, email)
VALUES (?, ?)
""", ("Paul", "paul@example.com"))

print(db_curseur.rowcount)

db_curseur.execute("""
SELECT id, nom, email
FROM utilisateurs
""")

db_utilisateurs = db_curseur.fetchall()

for utilisateur in db_utilisateurs:
    id_utilisateur, nom, email = utilisateur
    print(f"ID: {id_utilisateur} • {nom} • {email}")

# -> Commit des changements et fermeture de la connexion à la base de données
db_connexion.commit()
db_connexion.close()