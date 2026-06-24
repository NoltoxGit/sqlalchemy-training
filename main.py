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

db_telephones = db_curseur.fetchall()

for query_telephones in db_telephones:
    id_telephone = query_telephones[0]
    marque = query_telephones[1]
    modele = query_telephones[2]
    prix = query_telephones[3]

    print(f"{id_telephone} - {marque} {modele} : {prix} €")

connexion.commit()
connexion.close()