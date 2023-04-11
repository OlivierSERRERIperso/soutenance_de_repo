# --------------------- PROJET FIL ROUGE : PARTIE 2 : récupération des commentaires -------------------------
import warnings
warnings.filterwarnings("ignore")
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
# from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument("--headless")
options.add_argument("window-size=1400,1500")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("start-maximized")
options.add_argument("enable-automation")
options.add_argument("--disable-infobars")
options.add_argument("--disable-dev-shm-usage")

from time import sleep, time
import pandas as pd
import re
import numpy as np
import random
T_MIN = 1.5
T_MAX = 2
PAGE_NB = 3

# Instancitation du webdriver
try:
    driver = webdriver.Chrome(options=options)
except:
    driver = webdriver.Chrome(ChromeDriverManager().install())


def open_trust_pilot_and_close_cookie():
    # Ouverture d'une page TrustPilot
    driver.get('https://fr.trustpilot.com/')
    sleep(random.uniform(T_MIN, T_MAX))  # temps d'attente pour les cookies se chargent
    # Fermeture des cookies
    webelement = driver.find_element(by='id', value='onetrust-reject-all-handler')
    webelement.click()
    # à la fin de cette fonction on a trust pilot d'ouvert et les cookie ont été fermés


def get_clic_category(company):
    """
    recherche de l'entreprise
    """
    webelement = driver.find_element(by='class name', value="styles_searchInputField__Ltvjz")
    webelement.click()
    sleep(random.uniform(T_MIN, T_MAX))
    webelement.send_keys(company)
    sleep(random.uniform(T_MIN, T_MAX))
    webelement.send_keys(Keys.ENTER)
    sleep(random.uniform(T_MIN, T_MAX))


def get_informations_general_company():
    """
    On va récupérer les informations générales sur la company : nom, note, avis
    """
    sleep(random.uniform(T_MIN, T_MAX))
    try:
        name_company = driver.find_element(by='class name', value="typography_display-s__qOjh6").text
    except:
        name_company = None
    try:
        pourcentage_5_stars = driver.find_elements(by='class name', value="styles_row__wvn4i")[0].text.split('\n')[-1]
    except:
        pourcentage_5_stars = None
    try:
        pourcentage_4_stars = driver.find_elements(by='class name', value="styles_row__wvn4i")[1].text.split('\n')[-1]
    except:
        pourcentage_4_stars = None
    try:
        pourcentage_3_stars = driver.find_elements(by='class name', value="styles_row__wvn4i")[2].text.split('\n')[-1]
    except:
        pourcentage_3_stars = None
    try:
        pourcentage_2_stars = driver.find_elements(by='class name', value="styles_row__wvn4i")[3].text.split('\n')[-1]
    except:
        pourcentage_2_stars = None
    try:
        pourcentage_1_stars = driver.find_elements(by='class name', value="styles_row__wvn4i")[4].text.split('\n')[-1]
    except:
        pourcentage_1_stars = None
    try:
        avis_number = driver.find_element(by='class name', value="styles_header__yrrqf").text.split(":")[-1].strip().replace(' ', ' ')
    except:
        avis_number = None
    try:
        avis_notation = driver.find_element(by='class name', value="styles_header__yrrqf").text.split("Total")[0].split("Avis")[-1].strip()
    except:
        avis_notation = None

    print("-->" + str(name_company))
    print("-->" + str(pourcentage_5_stars))
    print("-->" + str(pourcentage_4_stars))
    print("-->" + str(pourcentage_3_stars))
    print("-->" + str(pourcentage_2_stars))
    print("-->" + str(pourcentage_1_stars))
    print("-->" + str(avis_number))
    print("-->" + str(avis_notation))
    print()
    return name_company, pourcentage_5_stars, pourcentage_4_stars, pourcentage_3_stars, pourcentage_3_stars, \
           pourcentage_1_stars, avis_number, avis_notation


def get_informations_comments(list_comment, n, l1, l2, l3, l4, l5, l6, l7, l8, l9, l10):
    """
    On va récupérer toutes les informations du commentaire : (10 informations pour être précis)
    TITRE COMMENTAIRE
    DATE EXPERIENCE
    COMMENTAIRE
    QUI A COMMENTÉ
    NOMBRE AVIS LAISSÉ PAR CETTE PERSONNE
    LOCALISATION DE LA PERSONNE QUI A COMMENTÉ
    PRÉSENCE D'UNE RÉPONSE (booléen)
    QUI A RÉPONDU
    RÉPONSE AU COMMENTAIRE
    NOMBRE D'ÉTOILE
    """
    # TITRE COMMENTAIRE
    try:
        title_comment_personne = list_comment[n].find_element(by='class name', value="typography_heading-s__f7029").text
    except:
        title_comment_personne = None

    # DATE EXPERIENCE
    try:  # obtention d'une liste de 3 ou 4 éléments avec la date en 2 ou 3 / mais aussi une liste de 1 élément -> bug
        list_date = list_comment[n].find_element(by='class name', value="styles_reviewContentwrapper__zH_9M").\
             find_elements(by='class name', value="typography_body-m__xgxZ_")
    except:
        date_experience = None
    else:
        try:
            test = list_date[1].text.find("Date de l'expérience:")
        except:
            date_experience = None
        else:
            if test == 0:  # c'est que la données de la date est en 2éme position
                date_experience = list_date[1].text.split(":")[-1].strip(" ")
            else:  # c'est que la données de la date est en 3éme position
                date_experience = list_date[2].text.split(":")[-1].strip(" ")

    # COMMENTAIRE
    try:
        comment_personne = list_comment[n].find_elements(by='class name', value="typography_body-l__KUYFJ")[0].text
    except:
        comment_personne = None

    # QUI A COMMENTÉ
    try:
        who_comment = list_comment[n].find_element(by='class name', value="styles_consumerDetailsWrapper__p2wdr").\
                find_element(by='class name', value="typography_heading-xxs__QKBS8").text
    except:
        who_comment = None

    # NOMBRE AVIS LAISSÉ PAR CETTE PERSONNE
    try:
        nb_who_comment = list_comment[n].find_element(by='class name', value="styles_consumerDetailsWrapper__p2wdr").\
                find_elements(by='class name', value="typography_body-m__xgxZ_")[0].text
    except:
        nb_who_comment = None

    # LOCALISATION DE LA PERSONNE QUI A COMMENTÉ
    try:
        where_who_comment = list_comment[n].find_element(by='class name', value="styles_consumerDetailsWrapper__p2wdr").\
                find_elements(by='class name', value="typography_body-m__xgxZ_")[1].text
    except:
        where_who_comment = None

    # PRÉSENCE D'UNE RÉPONSE (booléen)
    reponse_bool = True
    try:  # si on y arrive c'est qu'il y a une réponse au commentaire
        reponse_comment_bool = list_comment[n].find_element(by='class name', value="styles_replyInfo__FYSje").\
                 text.split(" ")[2].split("\n")[0]
    except:
        print("--> Pas de réponse à ce commentaire")
        reponse_bool = False
        reponse_comment_bool = None
    else:
        print("--> Il y'a une réponse à ce commentaire")

    # RÉPONSE AU COMMENTAIRE
    try:
        reponse_comment = list_comment[n].find_element(by='class name', value="styles_content__Hl2Mi").\
                  find_elements(by='class name', value="typography_body-m__xgxZ_")[2].text
    except:
        reponse_comment = None

    # NOMBRE D'ÉTOILE
    balise_int = list_comment[n].find_element(by='class name', value="star-rating_starRating__4rrcf")  # balise en amont
    star_number = 0
    try:
        try_star = balise_int.find_element(By.XPATH, "img[@alt='Noté 1 sur 5 étoiles']")
    except:
        pass
    else:
        star_number = 1
    try:
        try_star = balise_int.find_element(By.XPATH, "img[@alt='Noté 2 sur 5 étoiles']")
    except:
        pass
    else:
        star_number = 2
    try:
        try_star = balise_int.find_element(By.XPATH, "img[@alt='Noté 3 sur 5 étoiles']")
    except:
        pass
    else:
        star_number = 3
    try:
        try_star = balise_int.find_element(By.XPATH, "img[@alt='Noté 4 sur 5 étoiles']")
    except:
        pass
    else:
        star_number = 4
    try:
        try_star = balise_int.find_element(By.XPATH, "img[@alt='Noté 5 sur 5 étoiles']")
    except:
        pass
    else:
        star_number = 5

    print("--> TITRE COMMENTAIRE : " + str(title_comment_personne))
    print("--> DATE EXPERIENCE : " + str(date_experience))
    print("--> COMMENTAIRE : " + str(comment_personne))
    print("--> QUI A COMMENTÉ : " + str(who_comment))
    print("--> NOMBRE AVIS LAISSÉ PAR CETTE PERSONNE : " + str(nb_who_comment))
    print("--> LOCALISATION DE LA PERSONNE QUI A COMMENTÉ : " + str(where_who_comment))
    print("--> PRÉSENCE D'UNE RÉPONSE (booléen) : " + str(reponse_bool))
    print("--> QUI A RÉPONDU : " + str(reponse_comment_bool))
    print("--> RÉPONSE AU COMMENTAIRE : " + str(reponse_comment))
    print("--> NOMBRE D'ÉTOILE : " + str(star_number))
    print()
    print()
    print()
    # il n'y a plus de condition sur le nombre d'étoile désormais
    l1.append(title_comment_personne)
    l2.append(date_experience)
    l3.append(comment_personne)
    l4.append(who_comment)
    l5.append(nb_who_comment)
    l6.append(where_who_comment)
    l7.append(reponse_bool)
    l8.append(reponse_comment_bool)
    l9.append(reponse_comment)
    l10.append(star_number)


def go_next_page():
    sleep(random.uniform(T_MIN, T_MAX))
    webelement = driver.find_element(by='name', value='pagination-button-next')
    driver.execute_script('arguments[0].click()', webelement)
    sleep(random.uniform(T_MIN, T_MAX))


def actions_fill_list(l1, l2, l3, l4, l5, l6, l7, l8, l9, l10):
    try:
        liste_informations = driver.find_elements(by='class name', value="styles_cardWrapper__LcCPA")
    except:
        print("on a pas réussi à récupérer la liste des commentaire")
    else:
        for i in range(len(liste_informations)):
            get_informations_comments(liste_informations, i, l1, l2, l3, l4, l5, l6, l7, l8, l9, l10)


# DEBUT DU PROGRAMME
t0 = time()  # début du chronomètre
# CLIQUE SUR L'ENTREPRISE VOULUE
open_trust_pilot_and_close_cookie()
sleep(random.uniform(T_MIN, T_MAX))
get_clic_category("Showroomprive.com")


# 1er CSV : RECUPERATION DES INFORMATIONS GENERALES DE LA COMPANY
sleep(random.uniform(T_MIN, T_MAX))
name_company, pou_5, pou_4, pou_3, pou_2, pou_1, avis_number, avis_notation = get_informations_general_company()

# REMPLISSAGE DF / CREATION DE CSV / pour les informations générales de la company observée
dictionnaire_df = {'Name_company': [name_company],
                   'Pourcentage de 5 étoiles': [pou_5],
                   'Pourcentage de 4 étoiles': [pou_4],
                   'Pourcentage de 3 étoiles': [pou_3],
                   'Pourcentage de 2 étoiles': [pou_2],
                   'Pourcentage de 1 étoiles': [pou_1],
                   'Nombre avis': [avis_number],
                   "Notation": [avis_notation]}
df_company = pd.DataFrame(data=dictionnaire_df)
df_company.to_csv("scraping/PART2_Infos_Showroomprivee_Soutenance.csv")  # ON GARDERA T_MIN = 2 / T_MAX = 3


# 2eme CSV : RECUPERATION DES INFORMATIONS SUR LES COMMENTAIRES
liste_titre = []
liste_date = []
liste_commentaire = []
liste_qui_a_commente = []
liste_nombre_davis_laisse_par_cette_personne = []
liste_localisation_de_la_personne_qui_a_commente = []
liste_presence_dune_reponse_booleen = []
liste_qui_a_repondu = []
liste_reponse_au_commentaire = []
liste_nombre_detoile = []

nombre_page = PAGE_NB

for i in range(nombre_page):
    actions_fill_list(liste_titre,
                      liste_date,
                      liste_commentaire,
                      liste_qui_a_commente,
                      liste_nombre_davis_laisse_par_cette_personne,
                      liste_localisation_de_la_personne_qui_a_commente,
                      liste_presence_dune_reponse_booleen,
                      liste_qui_a_repondu,
                      liste_reponse_au_commentaire,
                      liste_nombre_detoile)
    print("Nombre de commentaire récupérés : " + str(len(liste_titre)))
    print("Page : " + str(i+1) + " / " + str(nombre_page))
    ti = time() - t0  # heure intermédiaire
    print("Réalisé en {} secondes".format(round(ti, 1)))
    print("Réalisé en {} minutes ".format(round(ti, 1) // 60))
    print()

    # REMPLISSAGE DF / CREATION DE CSV / pour les informations générales des commentaires négatifs
    # on effectue cela à chaque page que l'on récupère pour avoir un fichier .csv
    # si le programme plante avant la fin pour les informations générales de la company observée
    dictionnaire_infos_generales_comment = {"TITRE COMMENTAIRE": liste_titre,
                                            "DATE EXPERIENCE": liste_date,
                                            "COMMENTAIRE": liste_commentaire,
                                            "QUI A COMMENTÉ": liste_qui_a_commente,
                                            "NOMBRE AVIS LAISSÉ PAR CETTE PERSONNE": liste_nombre_davis_laisse_par_cette_personne,
                                            "LOCALISATION DE LA PERSONNE QUI A COMMENTÉ": liste_localisation_de_la_personne_qui_a_commente,
                                            "PRÉSENCE D'UNE RÉPONSE (booléen)": liste_presence_dune_reponse_booleen,
                                            "QUI A RÉPONDU": liste_qui_a_repondu,
                                            "RÉPONSE AU COMMENTAIRE": liste_reponse_au_commentaire,
                                            "NOMBRE D'ÉTOILE": liste_nombre_detoile}

    df_infos_generales_comment = pd.DataFrame(data=dictionnaire_infos_generales_comment)
    df_infos_generales_comment.to_csv("scraping/PART2_Infos_Soutenance.csv")

    go_next_page()


# CALCUL DU TEMPS DE REPONSE GLOBAL DU PROGRAMME
driver.close()
tt = time() - t0  # heure de fin
print("Réalisé en {} secondes".format(round(tt, 1)))
print("Réalisé en {} minutes ".format(round(tt, 1)//60))