# ---------------- PROJET FIL ROUGE : PARTIE 1 : récupération des entreprises de différents dommaines -------------------------
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
T_MIN = 2
T_MAX = 3
DATA_NUMBER_BY_PAGE = 2

# Instancitation du webdriver
try:
    driver = webdriver.Chrome(options=options)
except:
    driver = webdriver.Chrome(ChromeDriverManager().install())


def open_trust_pilot_and_close_cookie():
    # Ouverture d'une page TrustPilot
    driver.get('https://fr.trustpilot.com/')
    sleep(1)  # temps d'attente pour les cookies se chargent
    # Fermeture des cookies
    webelement = driver.find_element(by='id', value='onetrust-reject-all-handler')
    webelement.click()
    # à la fin de cette fonction on a trust pilot d'ouvert et les cookie ont été fermés


def get_clic_category(category):
    """
    Nous sommes sur la page principale, cette fonction a pour but de cliquer sur une des catégorie : banque par ex
    """
    webelement = driver.find_element(by='link text', value=category)
    webelement.click()


def get_infos_company(n_company):  # on va chager celle-ci pour ne récupérer qu'une seule liste désormais
    """
    Cette fonction a bout but de récupérer toutes les infos sur un compagny
    """
    list_name_score_avis_localisation_secteur = driver.find_elements(by='class name', value="paper_paper__1PY90")
    sleep(random.uniform(T_MIN, T_MAX))
    # N_societe = 14  # 14 (page 1) / 14 (page 2 ) / 58 (page 3) / 69 (page 3) / 124 (page 3) : test à effectuer
    print()
    print("Longueur de la liste des infos de la company : " + str(len(list_name_score_avis_localisation_secteur)))
    # 244 en général

    # BLOCS de Récupérations des infos : name, note, avis, localisation, etc ..
    try:
        company_name = list_name_score_avis_localisation_secteur[n_company].\
            find_element(by='class name', value="typography_heading-xs__jSwUz").text
    except:
        company_name = None
    try:
        trust_score_note = list_name_score_avis_localisation_secteur[n_company].\
            find_element(by='class name', value="styles_rating__pY5Pk").text.split("|")[0].split(" ")[-1]
    except:
        trust_score_note = None
    try:
        avis_nb = list_name_score_avis_localisation_secteur[n_company].\
            find_element(by='class name', value="styles_rating__pY5Pk").\
            text.split("|")[-1].split(" ")[0].replace(' ', ' ')
    except:
        avis_nb = None
    try:
        localisation = list_name_score_avis_localisation_secteur[n_company].\
            find_elements(by='class name', value="typography_body-m__xgxZ_")[2].text
    except:
        localisation = None
    try:
        secteur = list_name_score_avis_localisation_secteur[n_company].\
            find_elements(by='class name', value="styles_wrapper___E6__")[1].text
    except:
        secteur = None

    # CLIC sur le nom de la société pour récupérer le nombre d'avis excellent
    sleep(random.uniform(T_MIN, T_MAX))
    try:
        list_name_score_avis_localisation_secteur[3].click()
    except:
        print("ON N'A PAS REUSSI A CLIQUER SUR LA 1er COMPANY")
        sleep(random.uniform(T_MIN, T_MAX))
    else:
        print("--> Clique sur la 1er company")
        sleep(random.uniform(T_MIN, T_MAX))
        try:  # on essaye de récupérer une infos sur la page afin de vérifier que l'on a bien accès à celle-ci
            driver.find_elements(by='class name', value="styles_row__wvn4i")[0].text.split('\n')[-1]
        except:
            print("ON N'A PAS REUSSI A TROUVER l'ELEMENT SUR CETTE PAGE")
        else:
            sleep(random.uniform(T_MIN, T_MAX))
            driver.back()  # Si le 2 vérifications sont bonnes, c'est qu'on a réussi à accèder à la page --> driver.back

    sleep(random.uniform(T_MIN + 1, T_MAX + 1))

    try:
        list_name_score_avis_localisation_secteur[n_company].click()
    except:
        print("ON N'A PAS REUSSI A CLIQUER SUR LA BONNE COMPANY")
        avis_excellent = None
        sleep(random.uniform(T_MIN, T_MAX))
    else:
        print("--> Clique sur la company")
        sleep(random.uniform(T_MIN, T_MAX))
        try:  # on essaye de récupérer le nombre d'avis excellent
            avis_excellent = driver.find_elements(by='class name', value="styles_row__wvn4i")[0].text.split('\n')[-1]
        except:
            print("ON N'A PAS REUSSI A TROUVER l'ELEMENT SUR CETTE PAGE")
            avis_excellent = None  # on place alors l'élément "avis_excellent" à None
        sleep(random.uniform(T_MIN, T_MAX))
        driver.back()  # Si la vérification est bonne, c'est qu'on a réussi à accèder à la page --> driver.back

    print("INFOS COMPANY")
    print("name : " + str(company_name))
    print("note : " + str(trust_score_note))
    print("avis : " + str(avis_nb))
    print("loca : " + str(localisation))
    print("secteur : " + str(secteur))
    print("avis_exe : " + str(avis_excellent))
    return company_name, trust_score_note, avis_nb, localisation, secteur, avis_excellent
    # Le fait que l'on ne connaissent pas la longeur de la liste à l'PART1_avancement est plus complexe si le nombre d'élément au
    # sein d'un page est amené à changer. On récupère alors un nombre fixe de valeur à chaque fois


def filling_list_of_elements(list_name, list_note, list_avis, list_localisation, list_secteur, list_avis_excellent, nb_ele):
    """
    Cette liste a pour but de remplir des listes avec les informations recupérées dans les différentes pages
    On lui donne en entrée la liste des éléments récupéré sur la page et il ressort des liste aves les élements
    triés au bon endroit
    """
    for i in range(0, nb_ele):  # on veut : 3 / 14 / 25 / 36 / 47 car les infos des company sont a ces emplcacements
        name, note, avis, loca, sec, avis_ex,  = get_infos_company(3 + i*11)
        list_name.append(name)
        list_note.append(note)
        list_avis.append(avis)
        list_localisation.append(loca)
        list_secteur.append(sec)
        list_avis_excellent.append(avis_ex)
        print("Le nombre de données récupéré est : " + str(len(list_name)))
        print()
        sleep(random.uniform(T_MIN, T_MAX))
    return list_name, list_note, list_avis, list_localisation, list_secteur, list_avis_excellent


def get_info_category(categorie, n):
    """
    Cette fonction a pour but de réaliser les différents étapes pour récupérer les infos des companies d'une catégorie
    Dans celle-ci :
    On va aller sur la catégorie voulue
    On va récupérer le nombre de companies "n"
    On va aller sur la page suivante (page 2)
    On va récupérer le nombre de companies "n"
    On va aller sur la page suivante (page 3)
    On va récupérer le nombre de companies "n"
    On va retourner sur la page principale afin de pouvoir selectionner une autre catégorie en appelant de nouveau
    cette fonction
    """
    # CLIQUE SUR LA CATEGORIE BANQUE
    get_clic_category(categorie)
    sleep(random.uniform(T_MIN, T_MAX))
    print("On Clique sur la catégorie : " + str(categorie))

    # ON RECUPERE UN NOMBRE DONNEE DE VALEURS
    filling_list_of_elements(list_name, list_note, list_avis, list_localisation, list_secteur, list_avis_excellent, n)

    # ON VA SUR LA PAGE SUIVANTE
    sleep(random.uniform(T_MIN, T_MAX))
    webelement = driver.find_element(by='name', value='pagination-button-next')
    driver.execute_script('arguments[0].click()', webelement)
    sleep(random.uniform(T_MIN, T_MAX))

    # ON RECUPERE UN NOMBRE DONNEE DE VALEURS
    filling_list_of_elements(list_name, list_note, list_avis, list_localisation, list_secteur, list_avis_excellent, n)

    # ON VA SUR LA PAGE SUIVANTE
    sleep(random.uniform(T_MIN, T_MAX))
    webelement = driver.find_element(by='name', value='pagination-button-next')
    driver.execute_script('arguments[0].click()', webelement)
    sleep(random.uniform(T_MIN, T_MAX))

    # ON RECUPERE UN NOMBRE DONNEE DE VALEURS
    filling_list_of_elements(list_name, list_note, list_avis, list_localisation, list_secteur, list_avis_excellent, n)

    # ON REVIENT A LA PAGE PRINCIPALE
    sleep(random.uniform(T_MIN, T_MAX))
    driver.back()
    sleep(random.uniform(T_MIN, T_MAX))
    driver.back()
    sleep(random.uniform(T_MIN, T_MAX))
    driver.back()
    sleep(random.uniform(T_MIN, T_MAX))


t0 = time()  # heure du début / va permettre de calculer le temps qu'à mis le programme pour fonctionner

# OUVERTURE DE LA PAGE
open_trust_pilot_and_close_cookie()
sleep(random.uniform(T_MIN, T_MAX))

# CREATION DES LISTES # on initialise des listes vides
list_name = []
list_note = []
list_avis = []
list_localisation = []
list_secteur = []
list_avis_excellent = []

# Nombre de données à récupérer par page
m = DATA_NUMBER_BY_PAGE
liste_categorie_page_1 = ["Banques",
                          "Bijouterie",
                          "Animalerie",
                          "Magasin de vêtements",
                          "Concessionnaire automobile",
                          "Agents immobiliers",
                          "Magasin de meubles",
                          "Fitness et nutrition",
                          "Agence d'assurance"]

# On ne fait pas "assurance voyage" car il n'y a que une page de 11 avis
# On ne fait pas "fournisseur d'electricité" car il n'y a que une page de 11 avis
# On ne fait pas "magasin de meuble de chambre à coucher" car il n'y a que une page de 11 avis
# On ne fait pas "magasin de courtier en hypothèques" car il n'y a que 2 pages

liste_categorie_random = ["Magasin de vêtements",
                          "Animalerie"]

# CLIQUE SUR LA CATEGORIE
for element in liste_categorie_random:
    get_info_category(element, m)
    sleep(random.uniform(T_MIN, T_MAX))


# REMPLISSAGE DF / CREATION DE CSV
dictionnaire_df = {'Name_company': list_name,
                   'Note trust pilot': list_note,
                   'Nombre avis': list_avis,
                   'Localisation company': list_localisation,
                   'Domaine d activité': list_secteur,
                   "nombre d'avis excellent": list_avis_excellent}
df_company = pd.DataFrame(data=dictionnaire_df)
print(df_company)
df_company.to_csv("scraping/PART1_Infos_Soutenance.csv")

# CALCUL DU TEMPS DE DU PROGRAMME
tt = time() - t0  # heure de fin
print("Réalisé en {} secondes".format(round(tt, 1)))
print("Réalisé en {} minutes ".format(round(tt, 1)//60))