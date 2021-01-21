# Exploiter-l-opendata-des-horaires-de-la-TAM

I) Définir les différentes tâches : 
- Commenter et documenter le script existant
- Rajouter des fonctionnalitées 
- Veiller à respecter la PEP (installer "Pylint")
- Intégrer une Log

II) Répartition des tâches :
- Indiquer fichier CSV à partir de son chemin et le charger dans la BDD 
- Téléharger CSV du site de la TAM en temps réel dans la BDD (fonction mettre à jour la base de donnée)
- Afficher les temps d'attente à un arrêt pour une ligne.
- Afficher les prochains passages à un arrêt donné
- Faire une log 
- Commenter et documenter(.README)




III) Explication du script :

On importe 
-Sqlite3 pour lire la bdd
-Argparse pour faire une liste de commande
-os  
-Système pour sys.exit
-Urllib request pour faire une requete de téléchargement pour la DB de la TAM
-Typing named tuple 
-logging pour la log

- La fonction clear_rows(cursor) n'est pas utilisé pour le moment
- Insert CSV row : créer la table
- Load_csv : Ouvrir la db, la lire ligne par ligne
- Remove table : si nouvelle table, supprime l'ancienne
- Create shéma : Créer la structure de la table (les colonnes, lignes..)
- Class files(NamedTuple): On creer un objet qui contient deux variables de type str
- csv_path correspond à chemin vers le ficher csv
- db_path correspond au nom de que l'on donne à la base de donnée que l'on veut creer

- Download : Importe le dossier DATA TAM
- Wainting time : temps d'attente a un arret avant le prochain passage pour un arret, une ligne et une destination donnée
- nextTram : Définit les 3 prochains trains ou bus à un arret donné 

- parser : définition des différents éléments donnés en ligne de commandes :
- db_path = chemin de la base de donnée
- csv_path = chemin du fichier csv


- def_main : 



IV) Guide d'utilisation :

La fonction -u permet de télécharger la base de donnée en .csv directement via site de la tam, 
et supprime la derniere base de donnée téléchargée. 

La fonction -t permet d’afficher le prochain tram dans votre terminal.  
Entrez « -t » suivi du nom de votre arrêt et de sa direction, exemple : -u -t 2 SABINES JACOU le Terminal affiche (21:37)

La fonction -n affiche les 3 prochains tramways ou bus à un arret donné
Entrez « -u, -t, -n » dans votre terminal 
