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
-os, système,
-Urllib request pour faire une requete de téléchargement pour la DB de la TAM
-Typing named tuple 
-logging pour la log

- La fonction clear_rows(cursor) :
cursor.execute sert à raw curser pour repartir à 0
- Insert CSV row : créer la table
- Load_csv : supprimer l'entête
- Remove table : si nouvelle table, supprime l'ancienne
- Create shéma : Importe les colonnes 
- Class files(NamedTuple): csv est le liens vers le fichier .CSV, l'autre le transforme en db et le renomme?
- Download : Importe le dossier DATA TAM
- Wainting time : temps d'attente a un arret
- def_main : Définit Argparse



IV) Guide d'utilisation :

Téléchargez la bdd > cd.\tam_proj> python.\nom du fichier

La fonction -u permet de télécharger la base de donnée en .csv directement via site de la tam, 
et supprime la derniere base de donnée téléchargée. 

La fonction -t permet d’afficher le prochain tram dans votre terminal.  
Entrez « -t » suivi du nom de votre arrêt et de sa direction, exemple : -u -t 2 SABINES JACOU le Terminal affiche (21:37)

La fonction -n affiche les 3 prochains tramway 
Entrez « -u, -t, -n » dans votre terminal 
