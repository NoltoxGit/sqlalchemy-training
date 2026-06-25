# -> Importation du module sqlite3 pour interagir avec la base de données SQLite en local
import sqlite3


# -> Création de la table "telephone" (si elle n'existe pas déjà)
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


# -> Création de la table "utilisateur" (si elle n'existe pas déjà)
def db_create_utilisateur(db_curseur):
    db_curseur.execute("""
    CREATE TABLE IF NOT EXISTS utilisateur (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nom TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE
    )
    """)


# -> Insertion de téléphones
def db_ajouter_telephones(db_curseur, marque, modele, prix):
    db_curseur.execute("""
    INSERT OR IGNORE INTO telephone (marque, modele, prix)
    VALUES (?, ?, ?)
    """, (marque, modele, prix))

    # print(f"Nombre de téléphones ajoutés dans la base de données : {db_curseur.rowcount}.")


# -> Affichage des téléphones
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
        print(f"ID: {id_telephone} • Le téléphone \"{marque} {modele}\" coûte {prix} €")


# -> Insertion d'un utilisateur
def db_ajouter_utilisateur(db_curseur, nom, email):
    db_curseur.execute("""
    INSERT OR IGNORE INTO utilisateur (nom, email)
    VALUES (?, ?)
    """, (nom, email))

    # print(f"Nombre d'utilisateurs ajoutés dans la base de données : {db_curseur.rowcount}.")


# -> Affichage des utilisateurs
def db_afficher_utilisateurs(db_curseur):
    db_curseur.execute("""
    SELECT id, nom, email
    FROM utilisateur
    """)

    db_utilisateurs = db_curseur.fetchall()

    for query_utilisateur in db_utilisateurs:
        id_utilisateur, nom, email = query_utilisateur
        print(f"ID: {id_utilisateur} • {nom} • {email}")


# -> Fonction principale du programme
def main():
    db_connexion = sqlite3.connect("sqlalchemy_training.db")
    db_curseur = db_connexion.cursor()

    db_create_telephone(db_curseur)
    db_create_utilisateur(db_curseur)

    db_ajouter_telephones(db_curseur, "Samsung", "Galaxy A55", 449)
    db_ajouter_telephones(db_curseur, "Samsung", "Galaxy Z Flip6", 1199)
    db_afficher_telephones(db_curseur, 0) # -> Affiche les téléphones dont le prix est supérieur à 0€

    db_ajouter_utilisateur(db_curseur, "Paul", "paul@example.com")
    db_afficher_utilisateurs(db_curseur)

    db_connexion.commit()
    db_connexion.close()


# -> Exécution de la fonction principale si le script est exécuté directement ;
main()