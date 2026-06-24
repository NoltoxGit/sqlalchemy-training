import sqlite3

connexion = sqlite3.connect("phones.db")
curseur = connexion.cursor()

curseur.execute("""
CREATE TABLE IF NOT EXISTS phones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    brand TEXT NOT NULL,
    model TEXT NOT NULL,
    price_eur INTEGER NOT NULL
)
""")

connexion.commit()
connexion.close()

print("La base de données vient d'être créée avec succès !")