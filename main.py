import wikipedia
import sqlite3

from models.famous import Famous


# Initialisation
# Paramètres: full_name (Optionnel, n'est complété que lorsque on recommence la recherche)
def sdev(full_name=None):
    # Si pas complété, on demande la saisie à l'utilisateur
    if full_name is None:
        full_name = input("Enter the fullname of someone famous : ")

    # Si la célébrité recherché est trouvé
    if check_full_name_input(full_name):
        # Récupération de la page concernant la célébrité
        famous_page = wikipedia.page(full_name)

        # SQL
        sql(Famous(full_name, famous_page.summary))
    else:
        # Récupération d'une suggestion par rapport à la saisie
        famous_suggest = wikipedia.suggest(full_name)

        # On demande à l'utilisateur si il veut recommencer avec la suggestion proposée
        restart = input(f"Did you mean {famous_suggest} ? (Y - N): ")

        # Lorsque l'utilisateur répond que oui
        if check_restart(restart):
            sdev(famous_suggest)


# Permet de vérifier si la célébrité à été trouvé
def check_full_name_input(full_name):
    famous_find = [famous.upper() for famous in wikipedia.search(full_name)]
    return full_name.upper() in famous_find


# Permet de savoir si l'utilisateur à demander de recommencer
def check_restart(is_restart):
    return is_restart.upper() == "Y"


# Base de données
def sql(famous):
    # Connexion à la base de données
    con = sqlite3.connect('sdev.sqlite')
    cur = con.cursor()

    # Création de la table famous_people si elle n'existe pas
    cur.execute('''CREATE TABLE IF NOT EXISTS famous_people
                    (id INTEGER  PRIMARY KEY, 
                    name VARCHAR, 
                    summary VARCHAR)''')

    # Insertion dans la table
    cur.execute('INSERT INTO famous_people(name, summary) VALUES (?,?)', [famous.name, famous.summary])

    # Sauvegarde en base de données
    con.commit()

    # Fermeture de la connexion avec la base de données
    con.close()


# Point d'entrée de l'application
if __name__ == '__main__':
    sdev()
