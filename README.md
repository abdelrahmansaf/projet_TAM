# Exploiter-l-opendata-des-horaires-de-la-TAM

1) Définir les différentes tâches : 
- Commenter et documenter le script existant
- Rajouter des fonctionnalités 
- Veiller à respecter la PEP (installer "Pylint")
- Intégrer une Log

2) Répartition des tâches :
d) Indiquer fichier CSV à partir de son chemin et le charger dans la BDD (ok)
e) Téléharger CSV du site de la TAM en temps réel dans la BDD (fonction mettre à jour la base de donnée)
b) Afficher les temps d'attente à un arrêt pour une ligne.
c) Afficher les prochains passages à un arrêt donné
f) Faire une log 
a) Commenter et documenter(.README)


Explication du script :
j'importe Sqlite3 pour lire la bdd
argparse pour faire une liste de commande
os, système, urllib request pour faire la fonction
et typing named tuple pour faire la fonction
logging pour faire la log

La fonction clear_rows(cursor)
cursor.execute sert à raw curser pour repartir à 0

Insert CSV row : créer la table
Load_csv : sans l'entête
Remove table : si nouvelle table supprime l'ancienne
Create shéma : j'importer les colonnes 
Class files(NamedTuple):
Download : Importer dossier DATA TAM
Wainting time : temps d'attente a un arret
def_main :

Guide d'utilisation :
Téléchargez la bdd > cd.\tam_proj> python.\nom du fichier

La fonction -u permet de télécharger la base de donnée en .csv directement via site de la tam, 
et supprime la derniere base de donnée téléchargée. 

La fonction -t permet d’afficher le prochain tram dans votre terminal.  
Entrez « -t » suivi du nom de votre arrêt et de sa direction, exemple : -u -t 2 SABINES JACOU le Terminal affiche (21:37)

La fonction -n affiche les 3 prochains tramway 
Entrez « -u, -t, -n » dans votre terminal 
