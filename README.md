# Exploiter-l-opendata-des-horaires-de-la-TAM

I) Définir les différentes tâches : 
- Rajouter des fonctionnalitées 
- Veiller à respecter la PEP
- Intégrer une Log
- Commenter et documenter le script existant

II) Répartition des tâches :
- Indiquer fichier CSV à partir de son chemin et le charger dans la BDD (Stéphanie, Abdulrahman, Adrian)
- Téléharger CSV du site de la TAM en temps réel dans la BDD avec la fonction mettre à jour la base de donnée (Stéphanie, Abdulrahman, Adrian)
- Afficher les temps d'attente à un arrêt pour une ligne (Abdulrahman, Adrian)
- Afficher les prochains passages à un arrêt donné (Stéphanie)
- Faire une log (Sarah)
- Commenter et documenter (Sarah)
- Pep (Sarah)




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



Guide d'utilisation :

I- CSV et BDD

Si vous avez déja une base de donnée indiquez le chemin de votre csv et de votre fichier base de donnée suivi des arguments de la partie II.

OU 

Assurez vous d'avoir une connexion pour charger la bdd depuis le site de la TAM dans votre terminal avec les commandes :
> python .\transport.py -u suivi des arguments de votre choix.
(La fonction -u permet de télécharger la base de donnée en .csv directement via site de la tam)
  


II- Les arguments 
-t :
  La fonction -t(time) permet d’afficher le prochain tram dans votre terminal.  
  Entrez « -t » suivi du nom de votre arrêt et de sa direction
  exemple : -u -t 2 SABINES JACOU le Terminal affiche (21:37)

-n :
  La fonction -n(next) affiche les 3 prochains tramways ou bus à un arret donné
  Entrez « -u, -t, -n » dans votre terminal 
  exemple : u -t -n JACOU
