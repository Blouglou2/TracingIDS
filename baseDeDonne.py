#!/usr/bin/env python
#! -*- coding : utf-8 -*-

import sqlite3



# TODO vérifier que le dossier data est bien dans le répertoirecourant


def initialisationDB(nomBdd):
    
    db = sqlite3.connect(nomBdd)
    cursor = db.cursor()
    cursor.execute(""" 
    CREATE TABLE IF NOT EXISTS ip(
        IPdevice TEXT,
        IPdest TEXT,
        PortSource TEXT,
        PortDest TEXT,
        NomProcessus TEXT,
        UNIQUE(IPdevice,IPdest,PortSource,PortDest,NomProcessus)
    )
    """)
    cursor.execute(""" 
    CREATE TABLE IF NOT EXISTS filename(
        evenement TEXT,
        filename TEXT,
        NomProcessus TEXT,
        UNIQUE(evenement,filename,NomProcessus)
    )
    """)
    cursor.execute(""" 
    CREATE TABLE IF NOT EXISTS parentChild(
        parent TEXT,
        child TEXT,
        NomProcessus TEXT,
        UNIQUE(parent,child,NomProcessus)
    )
    """)
    db.commit()
    db.close()


def afficherTables(nomBdd):
    db = sqlite3.connect(nomBdd)
    cursor = db.cursor()
    cursor.execute("""
    SELECT * FROM ip
    """)
    all_rows = cursor.fetchall()  # cursor incok fetchall automatically (for row in cursor  does work)
    print("IP :")
    for row in all_rows:
        # row[0] returns the index, row[1] returns the device IP,row[2] returns the source port and row[3] returns the dest port.
        print("{0} | {1} | {2} | {3} | {4}".format(row[0], row[1], row[2], row[3], row[4]))

    cursor.execute("""
    SELECT * FROM filename
    """)
    all_rows = cursor.fetchall()  # cursor incok fetchall automatically (for row in cursor  does work)
    print("Filename :")
    for row in all_rows:
        # row[0] returns the index, row[1] returns the device IP,row[2] returns the source port and row[3] returns the dest port.
        print("{0} | {1} | {2} ".format(row[0], row[1], row[2]))

    cursor.execute("""
    SELECT * FROM parentChild
    """)
    all_rows = cursor.fetchall()  # cursor incok fetchall automatically (for row in cursor  does work)
    print("ParentChild :")
    for row in all_rows:
        # row[0] returns the index, row[1] returns the device IP,row[2] returns the source port and row[3] returns the dest port.
        print("{0} | {1} | {2} ".format(row[0], row[1], row[2]))

    closeDB(db)


def closeDB(db):
    db.close()


def main():

    # initialisationDB("./data/database.db")
    afficherTables("./data/database.db")


if __name__ == '__main__':
     main()