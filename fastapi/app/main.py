from fastapi import FastAPI
import csv
from collections import Counter

api = FastAPI()

with open("csv.csv", 'r') as file:
    csvreader = csv.reader(file, delimiter=',')
    # On saute la première ligne (en-tête)
    next(csvreader)
    # On définit les variables
    total = 0
    count = 0
    commentaires = []
    for row in csvreader:
        # Colonne correspondante
        nb_etoiles = int(row[10])
        total += nb_etoiles
        # On incrémente le compteur de lignes
        count += 1
    # On parcourt les lignes du fichier
        # On récupère le commentaire dans la colonne correspondante
        commentaire = row[3]
        # On ajoute le commentaire à la liste
        commentaires.append(commentaire)

    # On calcule la moyenne
    moyenne = total / count
   # print(moyenne)

# On combine tous les commentaires en une seule chaîne de caractères
    texte_complet = " ".join(commentaires)
    # On transforme la chaîne de caractères en une liste de mots
    liste_mots = texte_complet.split()
    # On utilise la classe Counter pour compter les occurrences de chaque mot
    compteur_mots = Counter(liste_mots)
    # On affiche les 10 mots les plus fréquents
#print("Mots supérieurs à 4 caractères les plus fréquents :")
   # for mot, nb_occurrences in compteur_mots.most_common(100):
      #  if len(mot) > 4:
       #  print(f"{mot} : {nb_occurrences} occurrences")"""

@api.get('/Moyenne des avis')
def get_moyenne():

    return {
            'La moyenne des avis est : ', round(moyenne,2)
    }


@api.get('/Mots récurrents')
def get_mots_recurrents():
    with open("csv.csv", 'r') as file:
        csvreader = csv.reader(file, delimiter=',')
        commentaires = []
        liste_mots_recurrents = []
        for row in csvreader:
            commentaire = row[3]
            commentaires.append(commentaire)
    # On combine tous les commentaires en une seule chaîne de caractères
        texte_complet = " ".join(commentaires)
    # On transforme la chaîne de caractères en une liste de mots
        liste_mots = texte_complet.split()
    # On utilise la classe Counter pour compter les occurrences de chaque mot
        compteur_mots = Counter(liste_mots)
    # On affiche les 10 mots les plus fréquents
        print("Mots supérieurs à 4 caractères les plus fréquents :")
        for mot, nb_occurrences in compteur_mots.most_common(100):
            if len(mot) >4:
               liste_mots_recurrents.append([mot,nb_occurrences])
        return {"Mots avec leurs nombres d'occurences":liste_mots_recurrents}






from vaderSentiment_fr.vaderSentiment import SentimentIntensityAnalyzer

sentiment_intensity_analyzer = SentimentIntensityAnalyzer()
@api.get('/Analyse de sentiment')
def get_analyse(Commentaire):
    scores = sentiment_intensity_analyzer.polarity_scores(Commentaire)
    sentiment = ""
    prédiction = ""
    print(scores['compound'])
    if scores['compound'] > 0:
        sentiment = "positif"
    elif scores['compound'] < 0:
        sentiment = "négatif"
    else:
        sentiment = "neutre"
    if -1 <= scores['compound'] <= -0.6:
        prédiction = 1
    elif -0.6 <= scores['compound'] <= -0.2:
        prédiction = 2
    elif -0.2 <= scores['compound'] <= 0.2:
        prédiction = 3
    elif 0.2 <= scores['compound'] <= 0.6:
        prédiction = 4
    else:
        prédiction = 5

    return {

        'Votre commentaire est : ': Commentaire,
        'Le score de votre commentaire est : ': scores['compound'],
        'Le sentiment de votre commentaire est : ': sentiment,
        'Votre commentaire possederait une notation de ' : prédiction
    }
