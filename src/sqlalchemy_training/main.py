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



# -> Ajout des informations d'un téléphone dans la table "telephone"
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

# -> Récupération de l'ID d'un téléphone à partir de sa marque et de son modèle
def db_get_telephone_id_by_marque_modele(db_curseur, marque, modele):
    db_curseur.execute("""
    SELECT id
    FROM telephone
    WHERE marque = ? AND modele = ?
    """, (marque, modele))

    result = db_curseur.fetchone()

    if result is None:
        return None

    return result[0]



# -> Ajout des informations d'un utilisateur dans la table "utilisateur"
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

# -> Récupération de l'ID d'un utilisateur à partir de son email
def db_get_utilisateur_id_by_email(db_curseur, email):
    db_curseur.execute("""
    SELECT id
    FROM utilisateur
    WHERE email = ?
    """, (email,))

    result = db_curseur.fetchone()

    if result is None:
        return None

    return result[0]



# -> Ajout d'un favori dans la table "favori" en associant un utilisateur à un téléphone
def db_ajouter_favori(db_curseur, utilisateur_id, telephone_id):
    db_curseur.execute("""
    INSERT OR IGNORE INTO favori (utilisateur_id, telephone_id)
    VALUES (?, ?)
    """, (utilisateur_id, telephone_id))

    print(f"Favoris ajoutés : {db_curseur.rowcount}")



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
    db_ajouter_utilisateur(db_curseur, "Thomas", "contact@thomasdupont.dev")
    db_afficher_utilisateurs(db_curseur)

    # -> Ajout d'un favori pour l'utilisateur avec l'ID 1 et le téléphone avec l'ID 1
    db_ajouter_favori(db_curseur, 1, 1)

    utilisateur_id = db_get_utilisateur_id_by_email(
        db_curseur,
        "contact@paulmuller.dev"
    )

    telephone_id = db_get_telephone_id_by_marque_modele(
        db_curseur,
        "Samsung",
        "Galaxy A55"
    )

    if utilisateur_id is not None and telephone_id is not None:
        db_ajouter_favori(db_curseur, utilisateur_id, telephone_id)
    else:
        print("[DEBUG: FAVORI] Impossible d'ajouter le favori : utilisateur ou téléphone introuvable.")
    
    # -> Sauvegarde des changements et fermeture de la connexion à la base de données
    db_connexion.commit()
    db_connexion.close()



# -> Exécution de la fonction principale uniquement si ce fichier est lancé directement
if __name__ == "__main__":
    main()