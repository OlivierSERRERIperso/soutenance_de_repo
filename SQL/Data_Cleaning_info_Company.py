#!/usr/bin/env python
# coding: utf-8
import pandas as pd
import numpy as np
import os
import csv
from unidecode import unidecode

df=pd.read_csv('/var/lib/jenkins/workspace/soutenance/scraping/PART1_Infos_Soutenance_Full.csv')
df.head()
df=df.drop(df.columns[0], axis=1)
df.head()
df.columns
df.to_csv('/var/lib/jenkins/workspace/soutenance/SQL/info_company.csv',index=False)


# ouvrir le fichier CSV original et créer un nouveau fichier pour écrire les données modifiées
with open('/var/lib/jenkins/workspace/soutenance/SQL/info_company.csv', 'r', encoding='utf-8') as fichier_original,      open('/var/lib/jenkins/workspace/soutenance/SQL/info_company_sans_accents.csv', 'w', encoding='utf-8', newline='') as fichier_modifie:
     
    # créer un objet writer pour écrire les données modifiées
    writer = csv.writer(fichier_modifie, delimiter=',')

    # parcourir chaque ligne du fichier original, supprimer les accents et écrire les données modifiées dans le nouveau fichier
    reader = csv.reader(fichier_original)
    for ligne in reader:
        nouvelle_ligne = [unidecode(cellule) for cellule in ligne]
        writer.writerow(nouvelle_ligne)


df.shape
data=pd.read_csv('/var/lib/jenkins/workspace/soutenance/SQL/info_company_sans_accents.csv')
data.head()
data.insert(0, 'id', range(data.shape[0]))
data.head()
data['Note trust pilot'] = data['Note trust pilot'].str.strip('"')
data['Note trust pilot'] = data['Note trust pilot'].replace(',', '.', regex=True)
data['Nombre avis'] = data['Nombre avis'].str.replace(' ', '')
data.dtypes
data['Nombre avis']
data.head()
data.isna().sum()
data.shape
data.to_csv('/var/lib/jenkins/workspace/soutenance/SQL/info_company.csv',index=False)



