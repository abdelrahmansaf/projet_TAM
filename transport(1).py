import sqlite3
import argparse
import sys
import os
import urllib.request
from typing import NamedTuple

def clear_rows(cursor):
    cursor.execute("""DELETE FROM infoarret""")


def insert_csv_row(csv_row, cursor):
    cursor.execute("""INSERT INTO infoarret VALUES (?,?,?,?,?,?,?,?,?,?,?) """,
                   csv_row.strip().split(";"))


def load_csv(path, cursor):
    with open(path, "r") as f:
        # ignore the header
        f.readline()
        line = f.readline()
        # loop over the lines in the file
        while line:
            insert_csv_row(line, cursor)
            line = f.readline()

def remove_table(cursor):
    cursor.execute("""DROP TABLE infoarret""")

def create_schema(cursor):
    cursor.execute("""CREATE TABLE IF NOT EXISTS "infoarret" (
    "course"	INTEGER,
    "stop_code"	TEXT,
    "stop_id"	INTEGER, 
    "stop_name"	TEXT,
    "route_short_name"	TEXT,
    "trip_headsign"	TEXT,
    "direction_id"	INTEGER,
    "is_theorical" INTEGER,
    "departure_time"	TEXT,
    "delay_sec"	INTEGER,
    "dest_arr_code"	INTEGER
    );""")

# On creer un objet qui peut contient deux variables de type str
# csv_path correspond à chemin vers le ficher csv
# db_path correspond au nom de que l'on donne à la base de donnée que l'on veut creer
class my_paths(NamedTuple):
    csv_path : str
    db_path : str

#Fonction that takes no arguments and returns a path
#url points to .csv file to download at Tam's website 
#variable path is set to current directory and renames downloaded file to tam.csv
# returns downloaded file path         
def download_csv():
    url = 'https://data.montpellier3m.fr/sites/default/files/ressources/TAM_MMM_TpsReel.csv'
    path = my_paths(os.getcwd() + "/tam.csv", "tam.db")
    urllib.request.urlretrieve(url,path.csv_path)
    return path

parser = argparse.ArgumentParser("Script to interact with data from the TAM API")
parser.add_argument("-db_path", help="path to sqlite database")
parser.add_argument("-csv_path", help="path to csv file to load into the db")
parser.add_argument("-u", "--update", action="store_true", help="update realtime TAM database")
parser.add_argument("-t", "--time", help="time for the waiting")
parser.add_argument("-n", "--next", help="Next tramways")

def main():
    args = parser.parse_args()
    
    if args.update:
        path = download_csv()
        db_path = path.db_path
        csv_path = path.csv_path
    elif not args.csv_path or not args.db_path:
        print("Error : missing command line arguments")
        return 1
    else:
        db_path = args.db_path
        csv_path = args.csv_path
   
    conn = sqlite3.connect(db_path)

    if not conn:
        print("Error : could not connect to database {}".format(db_path))
        return 1

    c = conn.cursor()

    #cette fonction efface notre table
    #remove_table(c)
    create_schema(c)
    
    if args.update:
        load_csv(csv_path,c)
    else:
        load_csv(args.csv_path, c)

    #write changes to database
    conn.commit()
    conn.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
