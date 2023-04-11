import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import warnings
import gensim
warnings.filterwarnings('ignore')
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import f1_score
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
import matplotlib.pyplot as plt
#%matplotlib inline

# %matplotlib inline # ligne pour jupyter seulement 

import json
import networkx as nx
from nltk.tokenize import TweetTokenizer

print("//////////DEBUT/////////////////////////")

# df = pd.read_csv('../scraping/PART2_Infos_Soutenance_Full.csv', sep = ',')

df = pd.read_csv('/var/lib/jenkins/workspace/soutenance/scraping/PART2_Infos_Soutenance_Full.csv', sep = ',')

print(len(df))

df.head()

# Suppression de Unamed

df.drop('Unnamed: 0', axis = 1)

df.info()

missing_values = df.isna().sum()
print(missing_values)

df.dropna(how='any', subset=['TITRE COMMENTAIRE', 'DATE EXPERIENCE', 'LOCALISATION DE LA PERSONNE QUI A COMMENTÉ'], inplace=True)
missing_values2 = df.isna().sum()
print(missing_values2)


df['COMMENTAIRE TOT'] = df['TITRE COMMENTAIRE'].str.cat(df['COMMENTAIRE'], sep=' ')

commentaires = df['COMMENTAIRE TOT']
df = df.drop(['TITRE COMMENTAIRE','COMMENTAIRE', 'QUI A COMMENTÉ', 'Unnamed: 0'], axis = 1)

df.head()

print(commentaires)

from vaderSentiment_fr.vaderSentiment import SentimentIntensityAnalyzer

sentiment_intensity_analyzer = SentimentIntensityAnalyzer()

score = commentaires.apply(lambda x: sentiment_intensity_analyzer.polarity_scores(x))

scores = commentaires.apply(lambda x: sentiment_intensity_analyzer.polarity_scores(x)['compound'])

print(scores.shape)
print(type(scores))
# print(scores)
scores.describe()

df_score_commentaires = scores.to_frame()

df_score_commentaires["COMMENTAIRE TOT"].astype(float)
df_score_commentaires.info()
df_score_commentaires.head()

reponse = df['RÉPONSE AU COMMENTAIRE']

print(reponse)

sentiment_intensity_analyzer_r = SentimentIntensityAnalyzer()

reponse = reponse.fillna('')
score_r = reponse.apply(lambda x: sentiment_intensity_analyzer.polarity_scores(x))

sentiment_intensity_analyzer_r = SentimentIntensityAnalyzer()


score_reponses = reponse.apply(lambda x: sentiment_intensity_analyzer_r.polarity_scores(x))
scores_reponses = reponse.apply(lambda x: sentiment_intensity_analyzer_r.polarity_scores(x)['compound'])

print(scores_reponses.shape)
print(type(scores_reponses))
# print(scores)
scores_reponses.describe()

df_score_reponses = scores_reponses.to_frame()

df_score_reponses["RÉPONSE AU COMMENTAIRE"].astype(float)
df_score_reponses.info()
df_score_reponses.head()

#Définition des variables expplicatives et cibles

feats_cat = df.drop(['NOMBRE AVIS LAISSÉ PAR CETTE PERSONNE' ,'COMMENTAIRE TOT', 'DATE EXPERIENCE' , "RÉPONSE AU COMMENTAIRE"], axis=1)
feats_cat.shape

feats_cat.head()

df['NOMBRE AVIS LAISSÉ PAR CETTE PERSONNE'] = df['NOMBRE AVIS LAISSÉ PAR CETTE PERSONNE'].str.replace(' avis', '')


df_nb_avis = df[['NOMBRE AVIS LAISSÉ PAR CETTE PERSONNE']]

df_nb_avis.head(5)

df_nb_avis = df_nb_avis.astype(int)

df_nb_avis.info()

df_nb_avis.head()

# Convertir feats en DataFrame
#feats = pd.DataFrame(array_feats, columns=list(feats_int.columns) + ["SCORE COMMENTAIRE"] + ["SCORE REPONSE"])

# Afficher le DataFrame

#feats.drop("Unnamed: 0", axis=1)
feats_cat.head()
#feats_cat.info()


feats_cat.shape

feats_cat = feats_cat.reset_index(drop=True)
df_nb_avis = df_nb_avis.reset_index(drop=True)
df_score_commentaires = df_score_commentaires.reset_index(drop=True)
df_score_reponses = df_score_reponses.reset_index(drop=True)


feats = feats_cat.join([df_nb_avis, df_score_commentaires, df_score_reponses])
# feats = feats[feats["LOCALISATION DE LA PERSONNE QUI A COMMENTÉ"] == "FR"]


feats = feats[(feats["LOCALISATION DE LA PERSONNE QUI A COMMENTÉ"] == "FR") | (df["LOCALISATION DE LA PERSONNE QUI A COMMENTÉ"] == "BE")]

feats.drop
feats.head(10)
feats.shape

feats["LOCALISATION DE LA PERSONNE QUI A COMMENTÉ"].value_counts()

feats = feats.drop(feats[feats['LOCALISATION DE LA PERSONNE QUI A COMMENTÉ'] == 'MQ'].index)


feats["LOCALISATION DE LA PERSONNE QUI A COMMENTÉ"].value_counts()



target = feats[["NOMBRE D'ÉTOILE"]].astype(float)
target.head()
target.shape
target.info()


feats = feats.drop(["NOMBRE D'ÉTOILE"], axis=1)

feats.head(10)


feats.info()

#Séparation des variables en test et en entrainement
X_train, X_test, y_train, y_test = train_test_split(feats, target, test_size=0.25, random_state = 42)
# X_train.info()


counts_train = X_train['LOCALISATION DE LA PERSONNE QUI A COMMENTÉ'].value_counts()
print(counts_train)

counts_test = X_test['LOCALISATION DE LA PERSONNE QUI A COMMENTÉ'].value_counts()
print(counts_test)


X_test.head()


print('X_train : ', X_train.shape, 'y_train : ', y_train.shape,  'X_test : ', X_test.shape,  'y_test : ', y_test.shape)


index_test = X_test.index.tolist()


index_train = X_train.index.tolist()


# print(index_train)


df_index_test = pd.DataFrame({'index_initial_test': index_test})
df_index_train = pd.DataFrame({'index_initial_train': index_train})


df_index_test.shape


df_index_train.head()

from sklearn.preprocessing import OneHotEncoder

# Le paramètre drop permet d'éviter le problème de multicolinéarité
ohe = OneHotEncoder( drop="first", sparse=False)
cat = ['LOCALISATION DE LA PERSONNE QUI A COMMENTÉ', "PRÉSENCE D'UNE RÉPONSE (booléen)", "QUI A RÉPONDU"]


X_train_cat = X_train[cat]
X_train_cat_encoded = ohe.fit_transform(X_train_cat)
X_train_cat_encoded_df = pd.DataFrame(X_train_cat_encoded)

X_train_cat_encoded_df.head()


X_train_cat_encoded_df.shape


df_cat_train_enc_index = df_index_train.join(X_train_cat_encoded_df)
df_cat_train_enc_index = df_cat_train_enc_index.rename(columns={0: 'LOCALISATION DE LA PERSONNE QUI A COMMENTÉ', 1: "PRÉSENCE D'UNE RÉPONSE (booléen)", 2: "QUI A RÉPONDU"})
df_cat_train_enc_index = df_cat_train_enc_index.set_index('index_initial_train')
df_cat_train_enc_index.head()


df_cat_train_enc_index.shape


y_train.shape


X_test.shape


X_test_cat = X_test[cat]
X_test_cat_encoded = ohe.transform(X_test[cat])
X_test_cat_encoded_df = pd.DataFrame(X_test_cat_encoded)


X_test_cat_encoded_df.shape


y_test.shape


X_test_cat.head()


X_test_cat.shape


X_test_cat_encoded_df.head()


X_test_cat_encoded_df.shape


quant = ['NOMBRE AVIS LAISSÉ PAR CETTE PERSONNE', "COMMENTAIRE TOT", "RÉPONSE AU COMMENTAIRE"]
X_train_quant = X_train[quant]
X_test_quant = X_test[quant]


X_test_quant.shape

X_test_cat_encoded_df.head()


df_cat_test_enc_index = df_index_test.join(X_test_cat_encoded_df)
df_cat_test_enc_index = df_cat_test_enc_index.rename(columns={0: 'LOCALISATION DE LA PERSONNE QUI A COMMENTÉ', 1: "PRÉSENCE D'UNE RÉPONSE (booléen)", 2: "QUI A RÉPONDU"})
df_cat_test_enc_index = df_cat_test_enc_index.set_index('index_initial_test')
df_cat_test_enc_index.head()


df_cat_test_enc_index.shape

y_test.shape

X_test_quant.head()


X_test_quant.shape

X_train = df_cat_train_enc_index.join([X_train_quant])
X_test = df_cat_test_enc_index.join([X_test_quant])


X_train.head()

X_train.isna().sum()

X_test.head()

X_test.isna().sum()


X_test=X_test.dropna()

X_test.isna().sum()

# X_train_encode = pd.get_dummies(X_train[X_train.columns[:-1]], drop_first=True)
# X_train_encode.head(5)
# X_train_encode.info()

# col_ohe = ['NOMBRE AVIS LAISSÉ PAR CETTE PERSONNE', 'LOCALISATION DE LA PERSONNE QUI A COMMENTÉ', "PRÉSENCE D'UNE RÉPONSE (booléen)", "QUI A RÉPONDU"]

# fff = X_test[col_ohe]
# fff.head(10)
# fff.shape
# encoded_columns = ['Reponse ou non_encodé', 'Liste peronnes_encodé_1', 'Liste peronnes_encodé_2']

# # Encodage des colonnes 'Reponse ou non' et 'Liste peronnes'
# encoded_train = ohe.fit_transform(X_train[['Reponse ou non', 'Liste peronnes']])
# encoded_test = ohe.transform(X_test[['Reponse ou non', 'Liste peronnes']])

# # Assigner les nouvelles colonnes encodées à votre DataFrame d'entraînement
# X_train[encoded_columns] = encoded_train
# X_test[encoded_columns] = encoded_test

# # Supprimer les colonnes originales
# X_train = X_train.drop(['Reponse ou non', 'Liste peronnes'], axis=1)
# X_test = X_test.drop(['Reponse ou non', 'Liste peronnes'], axis=1)

# # Insérez votre code ici 
# from sklearn.preprocessing import OneHotEncoder

# # Le paramètre drop permet d'éviter le problème de multicolinéarité
# ohe = OneHotEncoder( drop="first", sparse=False)

# X_train.loc[:,['Reponse ou non', 'Liste peronnes']] = ohe.fit_transform(X_train[['Reponse ou non', 'Liste peronnes']])

# X_test.loc[:,['Reponse ou non', 'Liste peronnes']] = ohe.transform(X_test[['Reponse ou non', 'Liste peronnes']])

# X_test.head()

# Insérez votre code ici
from sklearn.tree import DecisionTreeClassifier

clf = DecisionTreeClassifier(max_depth = 3)

clf.fit(X_train, y_train)

score_train = clf.score(X_train, y_train)
score_test = clf.score(X_test, y_test)

print("score d'entrainement :", score_train, "////", "score de test :", score_test)


type(y_test)

print(y_test)


Tableau_test = X_test.join(y_test)
Tableau_test = Tableau_test.drop(Tableau_test[Tableau_test["NOMBRE D'ÉTOILE"].isin([3, 4, 5])].index)
Tableau_test = Tableau_test.dropna(how='any', axis=0)

y_test = Tableau_test["NOMBRE D'ÉTOILE"]
X_test = Tableau_test.drop("NOMBRE D'ÉTOILE", axis = 1)
Tableau_test


from sklearn.metrics import classification_report

y_pred = clf.predict(X_test)

# type(y_pred)
type(y_pred)


print(pd.crosstab(y_test.values,y_pred))
print(classification_report(y_test, y_pred))

crosstab_clf = pd.crosstab(y_test.values,y_pred)
crosstab_clf_str = crosstab_clf.to_string()

file = open("machine_learning/resultats.txt", "w") 
file.write(crosstab_clf_str)
file.close()



import warnings
warnings.filterwarnings('ignore')
import time
import pandas as pd
import numpy as np
import gensim
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.model_selection import train_test_split, GridSearchCV,cross_val_score
from sklearn.ensemble import GradientBoostingClassifier,RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from numba import jit


"""
rl = LogisticRegression()

# param_grid_rl = { 'C':[0.01,0.05,0.1], 'max_iter' : [50,75,100], "solver" : ["newton-cg", "lbfgs", "sag", "saga"]}
# grid_rl = GridSearchCV(estimator=rl, param_grid= param_grid_rl,cv=5, n_jobs = -1, refit=True).fit(X_train,y_train)
# print(grid_rl.best_params_)
# print(grid_rl.best_score_)
#  
#///////////////////////////////////////////////////////////////////////////////////////////////////////
# print("score d'entrainement :", score_train, "////", "score de test :", score_test)

# Tableau_test = X_test.join(y_test)
# Tableau_test = Tableau_test.drop(Tableau_test[Tableau_test["NOMBRE D'ÉTOILE"].isin([3, 4, 5])].index)
# Tableau_test = Tableau_test.dropna(how='any', axis=0)

# y_test = Tableau_test["NOMBRE D'ÉTOILE"]
# X_test = Tableau_test.drop("NOMBRE D'ÉTOILE", axis = 1)
# Tableau_test

# from sklearn.metrics import classification_report

# y_pred = clf.predict(X_test)

# # type(y_pred)
# type(y_pred)

# print(pd.crosstab(y_test.values,y_pred))
# print(classification_report(y_test, y_pred))

y_train = np.ravel(y_train)

print("//////////GradientBoostingClassifier/////////////////////////")

gb = GradientBoostingClassifier()
param_grid_gb = {"n_estimators":[200,300,400,500], "learning_rate":[0.25,0.5,0.75], "max_depth": [1,None]}
grid_gb = GridSearchCV(estimator=gb, param_grid= param_grid_gb,cv=5, n_jobs = -1, refit=True).fit(X_train,y_train)
print(grid_gb.best_params_)
print(grid_gb.best_score_) 



print("//////////RandomForestClassifier/////////////////////////")

rf = RandomForestClassifier()
param_grid_rf = {'max_features': ["sqrt", "log2", None], "criterion": ["gini", "entropy", "log_loss"],"max_depth" : [1,None]}
grid_rf = GridSearchCV(estimator=rf, param_grid= param_grid_rf,cv=5, n_jobs = -1, refit=True).fit(X_train,y_train)
print(grid_rf.best_params_)
print(grid_rf.best_score_) 


svc = SVC()
param_grid_svc = {'C':[0.01,0.05,0.1],"kernel" :["linear", "poly", "rbf", "sigmoid"],}
grid_svc = GridSearchCV(estimator=svc, param_grid= param_grid_svc,cv=5, n_jobs = -1, refit=True).fit(X_train,y_train)
print(grid_svc.best_params_)
print(grid_svc.best_score_) 
"""

tokenizer = TweetTokenizer()
texte = ' '.join(commentaires)
mots = tokenizer.tokenize(texte)
print(len(mots))

from collections import Counter

word_count = Counter([m.lower() for m in mots])

mots_tries = sorted(word_count, key=lambda x: word_count.get(x), reverse=True)


print(mots_tries)



mots_tries_string = ' / '.join(mots_tries)


file = open("machine_learning/mots_tries.txt", "w") 
file.write(mots_tries_string) 
file.close()

print("BIEN EXECUTE !!!!!")

