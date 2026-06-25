# -> Importation du module sqlite3 pour interagir avec une base de données SQLite locale
import sqlite3


# -> Création de la table "telephone" si elle n'existe pas déjà
def db_create_telephone(db_curseur):
    db_curseur.execute("""
    CREATE TABLE IF NOT EXISTS telephone (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        marque TEXT NOT NULL,
        modele TEXT NOT NULL,
        prix INTEGER NOT NULL,
        UNIQUE(marque, modele)
    )
    """)


# -> Création de la table "utilisateur" si elle n'existe pas déjà
def db_create_utilisateur(db_curseur):
    db_curseur.execute("""
    CREATE TABLE IF NOT EXISTS utilisateur (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE
    )
    """)


# -> Création de la table "favori" si elle n'existe pas déjà
def db_create_favori(db_curseur):
    db_curseur.execute("""
    CREATE TABLE IF NOT EXISTS favori (
        utilisateur_id INTEGER NOT NULL,
        telephone_id INTEGER NOT NULL,
        PRIMARY KEY (utilisateur_id, telephone_id),
        FOREIGN KEY (utilisateur_id) REFERENCES utilisateur(id),
        FOREIGN KEY (telephone_id) REFERENCES telephone(id)
    )
    """)

# -> Insertion d'un téléphone
def db_ajouter_telephone(db_curseur, marque, modele, prix):
    db_curseur.execute("""
    INSERT OR IGNORE INTO telephone (marque, modele, prix)
    VALUES (?, ?, ?)
    """, (marque, modele, prix))


# -> Affichage des téléphones dont le prix est supérieur à un prix minimum
def db_afficher_telephones(db_curseur, prix_minimum):
    db_curseur.execute("""
    SELECT id, marque, modele, prix
    FROM telephone
    WHERE prix > ?
    ORDER BY prix DESC
    """, (prix_minimum,))

    db_telephones = db_curseur.fetchall()

    for query_telephone in db_telephones:
        id_telephone, marque, modele, prix = query_telephone
        print(f"[DEBUG: PHONE] ID: {id_telephone} • Le téléphone \"{marque} {modele}\" coûte {prix} €.")


# -> Insertion d'un utilisateur
def db_ajouter_utilisateur(db_curseur, nom, email):
    db_curseur.execute("""
    INSERT OR IGNORE INTO utilisateur (nom, email)
    VALUES (?, ?)
    """, (nom, email))


# -> Affichage des utilisateurs
def db_afficher_utilisateurs(db_curseur):
    db_curseur.execute("""
    SELECT id, nom, email
    FROM utilisateur
    """)

    db_utilisateurs = db_curseur.fetchall()

    for query_utilisateur in db_utilisateurs:
        id_utilisateur, nom, email = query_utilisateur
        print(f"[DEBUG: USER] ID: {id_utilisateur} • L'utilisateur \"{nom}\" a pour email \"{email}\".")


# -> Fonction principale du programme
def main():
    # -> Connexion à la base de données SQLite
    db_connexion = sqlite3.connect("sqlalchemy_training.db")
    db_connexion.execute("PRAGMA foreign_keys = ON") # -> Activation de la vérification des clés étrangères
    db_curseur = db_connexion.cursor()

    # -> Création des tables dans la base de données
    db_create_telephone(db_curseur)
    db_create_utilisateur(db_curseur)
    db_create_favori(db_curseur)

    # -> Ajout de téléphones et d'utilisateurs, puis affichage des résultats
    db_ajouter_telephone(db_curseur, "Samsung", "Galaxy A55", 399)
    db_ajouter_telephone(db_curseur, "Samsung", "Galaxy Z Flip6", 1199)
    db_afficher_telephones(db_curseur, 0) # -> Affiche les téléphones dont le prix est supérieur à 0€

    # -> Ajout d'un utilisateur et affichage des utilisateurs
    db_ajouter_utilisateur(db_curseur, "Paul", "contact@paulmuller.dev")
    db_afficher_utilisateurs(db_curseur)

    db_connexion.commit()
    db_connexion.close()


# -> Exécution de la fonction principale uniquement si ce fichier est lancé directement
if __name__ == "__main__":
    main()