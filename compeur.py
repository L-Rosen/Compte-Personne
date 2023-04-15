# Import des bibliothèques nécessaires
import RPi.GPIO as GPIO  # Bibliothèque pour contrôler les broches GPIO d'un Raspberry Pi
import time  # Bibliothèque pour le temps
import sqlite3  # Bibliothèque pour interagir avec une base de données SQLite

# Fonction qui incrémente le compteur dans la base de données
def incr():
    # Requête SQL pour incrémenter la valeur dans la base de données
    sqlite_select_Query = """UPDATE compeurDB SET nombre_de_personne = nombre_de_personne + 1 WHERE id=1;"""
    # Exécution de la requête SQL avec le curseur
    cursor.execute(sqlite_select_Query)
    # Validation de la transaction avec la base de données
    sqliteConnection.commit()

# Fonction qui décrémente le compteur dans la base de données
def decr():
    # Requête SQL pour décrémenter la valeur dans la base de données
    cursor.execute("""SELECT nombre_de_personne FROM compeurDB WHERE id=1;""")
    resultat = cursor.fetchone()[0]
    if resultat > 0 :
        sqlite_select_Query = """UPDATE compeurDB SET nombre_de_personne = nombre_de_personne - 1 WHERE id=1;"""
        cursor.execute(sqlite_select_Query)
        sqliteConnection.commit()

# Connexion à la base de données
sqliteConnection = sqlite3.connect('db.sqlite',check_same_thread=False)
# Création d'un curseur pour interagir avec la base de données
cursor = sqliteConnection.cursor()

# Configuration des broches GPIO
DIO2 = 4  # Numéro de la broche GPIO à utiliser pour le bouton 1
DIO1 = 16  # Numéro de la broche GPIO à utiliser pour le bouton 2

# Configuration du mode et de la résistance de rappel des broches GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(DIO2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
GPIO.setup(DIO1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

# Initialisation des flag et du temps
compeur = 0
timer = False
flag1 = False
flag2 = False

# Fonction d'interruption pour le bouton 1
def interrupt1(channel):
    global timer
    global compeur
    global flag1
    global flag2
    print('Bouton 1')
    # Si aucun drapeau n'est levé
    if not flag1 and not flag2:
         flag1 = True  # Lever le drapeau pour indiquer que le bouton 1 a été pressé
         timer = True
         compeur = 0
    # Si le drapeau pour le bouton 2 est levé
    elif flag2:
        incr()  # Incrémenter le compteur dans la base de données
        flag1 = False  # Abaisser le drapeau pour indiquer que le traitement est terminé
        flag2 = False  # Abaisser le drapeau pour indiquer que le bouton 2 est maintenant libre

# Fonction d'interruption pour le bouton 2
def interrupt2(channel):
    global compeur
    global timer
    global flag1
    global flag2
    print('Bouton 2')
    # Si aucun drapeau n'est levé
    if not flag1 and not flag2:
        flag2 = True  # Lever le drapeau pour indiquer que le bouton 2 a été appuyé
        timer = True
        compeur = 0
    # Si le drapeau pour le bouton 1 est levé
    elif flag1:
        decr()  # Décrémenter le compteur dans la base de données
        flag1 = False  # Abaisser le drapeau pour indiquer que le traitement est terminé
        flag2 = False  # Abaisser le drapeau pour indiquer que le bouton 1 est maintenant libre

# Configuration de l'interruption pour les broches GPIO
GPIO.add_event_detect(DIO2, GPIO.RISING, callback=interrupt1, bouncetime=300)
GPIO.add_event_detect(DIO1, GPIO.RISING, callback=interrupt2, bouncetime=300)

# Boucle principale
while True:
    time.sleep(0.1)  # Attente de 0,1 seconde avant de recommencer la boucle
    if timer == True:
        compeur +=0.1
        print(compeur)
    if compeur >0.5:
        flag1 = flag2 = False
        timer = False
        compeur = 0
