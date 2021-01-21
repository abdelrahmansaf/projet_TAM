import sqlite3
import argparse
import sys
import os
import urllib.request
import math
from typing import NamedTuple

# def clear_rows(cursor):
#     cursor.execute("""DELETE FROM infoarret""")


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
    cursor.execute("""DROP TABLE IF EXISTS infoarret""" )

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

# On creer un objet qui contient deux variables de type str
# csv_path correspond à chemin vers le ficher csv
# db_path correspond au nom de que l'on donne à la base de donnée que l'on veut creer
class files(NamedTuple):
    csv_path : str
    db_path : str

#Fonction that takes no arguments and returns a path
#url points to .csv file to download at Tam's website 
#variable path is set to current directory and renames downloaded file to tam.csv
# returns downloaded file path         
def download_csv():
    url = 'https://data.montpellier3m.fr/sites/default/files/ressources/TAM_MMM_TpsReel.csv'
    files_paths = files(os.getcwd() + "/tam.csv", "tam.db")
    urllib.request.urlretrieve(url,files_paths.csv_path)
    return files_paths

def waiting_time(route_short_name,stop_name,trip_headsign,table_path,cursor):
    cursor.execute(f"SELECT is_theorical FROM {table_path} WHERE route_short_name = '{route_short_name}' AND stop_name = '{stop_name}' AND trip_headsign = '{trip_headsign}' LIMIT 1")
    return cursor.fetchone()

def nextTram(stop_name, table_name, cursor):
    cursor.execute(f"SELECT * FROM {table_name} WHERE stop_name = '{stop_name}' ORDER BY delay_sec")
    i=0
    trip_list =[]
    for next_trip in cursor.fetchall():
        trip_list.append(f"La ligne {next_trip[4]} à destination de {next_trip[5]} arrive dans {(math.ceil(next_trip[9]/60))} minutes")
        i+=1
        if i>=3:
            break
    return trip_list


parser = argparse.ArgumentParser("Script to interact with data from the TAM API")
parser.add_argument("-db", "--db_path", help="path to sqlite database")
parser.add_argument("-csv", "--csv_path", help="path to csv file to load into the db")
parser.add_argument("-u", "--update", action="store_true", help="update realtime TAM database")
parser.add_argument("-t", "--time", nargs="*", help="time for the waiting")
parser.add_argument("-n", "--next", help="Next tramways")
parser.add_argument("-f", "--file",action="store_true", help="Write on file")

def main():
    args = parser.parse_args()
    
    if args.update:
        files_paths = download_csv()
        db_path = files_paths.db_path
        csv_path = files_paths.csv_path
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
    #this fonction removes our table
    remove_table(c)
    
    #this fonction creates a structure for our database 
    create_schema(c) 
    
    if not args.file:
        if args.next and (args.update or (args.db_path and args.csv_path)):
            load_csv(csv_path,c)
            for trip in nextTram(args.next, "infoarret",c):
                print(trip)
        elif args.time and (args.update or (args.db_path and args.csv_path)):
            load_csv(csv_path,c)
            print("Le prochain tram arrive à :","".join(list(waiting_time(args.time[0],args.time[1],args.time[2],"infoarret",c))))     
        else:
            load_csv(args.csv_path, c)
    else:
        info_tam = open("info_tam.txt", "a",encoding='utf-8')
        if args.next and (args.update or (args.db_path and args.csv_path)):
            load_csv(csv_path,c)
            for trip in nextTram(args.next, "infoarret",c):
                info_tam.write(f"{trip}\n")
        elif args.time and (args.update or (args.db_path and args.csv_path)):
            load_csv(csv_path,c)
            info_tam.write("Le prochain tram arrive à :" + "".join(list(waiting_time(args.time[0],args.time[1],args.time[2],"infoarret",c)))+"\n") 
        else:
            load_csv(args.csv_path, c)
        info_tam.close()

    #write changes to database
    conn.commit()
    conn.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
