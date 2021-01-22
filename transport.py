""" Import :
Sqlite3 t read bdd
Argparse to do a list command
os
Système for sys.exit
Urllib request to do a download request for the TAM db
Typing named tuple
logging for the log """

import sqlite3
import argparse
import sys
import logging
import os
import urllib.request
import math
import time
from tqdm import tqdm
from typing import NamedTuple

""" Logging implementation """
logging.basicConfig(filename="logtransport.log", level=logging.INFO,
 format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')


# def loading_screen():
#     for _ in tqdm(range(100),
#      desc="Downloading files and creating database...",
#      ascii=False, ncols=100):
#         time.sleep(0.01)

""" insert_csv_row create a table function """
logging.info("Create table")

#Fill out the Data Base
def insert_csv_row(csv_row, cursor):
    cursor.execute("""INSERT INTO infoarret VALUES (?,?,?,?,?,?,?,?,?,?,?) """,
                   csv_row.strip().split(";"))


""" load_csv function to open db, read line by line"""
logging.info("Open db, read line by line")


def load_csv(path, cursor):
    with open(path, "r") as f:
        # ignore the header
        f.readline()
        line = f.readline()
        # loop over the lines in the file
        while line:
            insert_csv_row(line, cursor)
            line = f.readline()


""" Remove_table function wich delete a table if it found one """
logging.info("if a table is find, delete it")

# Removing table from DB
def remove_table(cursor):
    cursor.execute("""DROP TABLE IF EXISTS infoarret""" )


""" Fonction create_shema to create the structure, lines and columns.."""
logging.info("Create the structure, lines and columns..")


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


""" The class files(NamedTuple) fonction create an object with two types of str values,
one "csv_path", it correspond to the file csv path
the second for the bdd name db_path """

logging.info("We create an object wich contain two str table value")


class files(NamedTuple):
    csv_path: str
    db_path: str


"""download_csv function that takes no arguments and returns a path
url points to .csv file to download at Tam's website
variable path is set to current directory and renames downloaded file to tam.csv
returns downloaded file path"""


logging.info("Import DATA TAM file")


def download_csv():
    # loading_screen()
    url = 'https://data.montpellier3m.fr/sites/default/files/ressources/TAM_MMM_TpsReel.csv'
    files_paths = files(os.getcwd() + "/tam.csv", "tam.db")
    urllib.request.urlretrieve(url,files_paths.csv_path)
    print("Database created successfully!")
    return files_paths


""" waiting_time function allows the waiting time before the next trip for a stop, line and destinaton."""
logging.info("waiting time before the next trip for a stop, line and destinaton.")


def waiting_time(route_short_name,stop_name,trip_headsign,table_path,cursor):
    cursor.execute(f"SELECT is_theorical FROM {table_path} WHERE route_short_name = '{route_short_name}' AND stop_name = '{stop_name}' AND trip_headsign = '{trip_headsign}' LIMIT 1")
    return cursor.fetchone()


"""nextTram function defined the next 3 trains or bus for a stop"""
logging.info("Defind the next 3 trains or bus for a stop")


def nextTram(stop_name, table_name, cursor):
    cursor.execute(f"SELECT * FROM {table_name} WHERE stop_name = '{stop_name}' ORDER BY delay_sec")
    i=0
    trip_list =[]
    for next_trip in cursor.fetchall():
        trip_list.append(f"The ligne {next_trip[4]} Destination to {next_trip[5]} Is coming in {(math.ceil(next_trip[9]/60))} minutes")
        i+=1
        if i>=3:
            break
    return trip_list


"""parser : defined the differents elements given in the command line
db_path = path to the bdd
csv_path = path to the csv file"""


logging.info("definition off the differents elements given in the command line:")
parser = argparse.ArgumentParser("Script to interact with data from the TAM API")
parser.add_argument("-db", "--db_path", help="path to sqlite database")
parser.add_argument("-csv", "--csv_path", help="path to csv file to load into the db")
parser.add_argument("-u", "--update", action="store_true", help="update realtime TAM database")
parser.add_argument("-t", "--time", nargs="*", help="time for the waiting")
parser.add_argument("-n", "--next", help="Next tramways")
parser.add_argument("-f", "--file", action="store_true", help="Write on file")


""" main function defined the body program """
logging.info("fonction corps du programme")


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
    """this fonction removes our table"""
    remove_table(c)

    """this fonction creates a structure for our database"""
    create_schema(c)

    if not args.file:
        if args.next and (args.update or (args.db_path and args.csv_path)):
            load_csv(csv_path,c)
            for trip in nextTram(args.next.upper(), "infoarret",c):
                print(trip)
        elif args.time and (args.update or (args.db_path and args.csv_path)):
            load_csv(csv_path,c)
            print("The next tram-way in:","".join(list(waiting_time(args.time[0],args.time[1].upper(),args.time[2].upper(),"infoarret",c))))     
        else:
            load_csv(args.csv_path, c)
    else:
        info_tam = open("info_tam.txt", "a",encoding='utf-8')
        if args.next and (args.update or (args.db_path and args.csv_path)):
            load_csv(csv_path,c)
            for trip in nextTram(args.next.upper(), "infoarret",c):
                info_tam.write(f"{trip}\n")
        elif args.time and (args.update or (args.db_path and args.csv_path)):
            load_csv(csv_path,c)
            info_tam.write("The next tram-way in:" + "".join(list(waiting_time(args.time[0],args.time[1].upper(),args.time[2].upper(),"infoarret",c)))+"\n") 
        else:
            load_csv(args.csv_path, c)
        info_tam.close()

    """write changes to database"""
    conn.commit()
    conn.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())