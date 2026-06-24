import sqlite3

connexion = sqlite3.connect("phones.db")
db_curseur = connexion.cursor()

db_curseur.execute("""
CREATE TABLE IF NOT EXISTS phones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    marque TEXT NOT NULL,
    modele TEXT NOT NULL,
    prix INTEGER NOT NULL
)
""")

db_curseur.execute("""
INSERT INTO phones (marque, modele, prix)
VALUES (?, ?, ?)
""", ("Samsung", "Galaxy S24", 899))

db_curseur.execute("""
SELECT id, marque, modele, prix
FROM phones
WHERE prix > ?
""", (800,))

telephones = db_curseur.fetchall()

for telephone in telephones:
    print(telephone)

connexion.commit()
connexion.close()