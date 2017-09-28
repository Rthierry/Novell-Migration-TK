#!/usr/bin/env python3

import csv
import sys
import codecs
import getopt
import pandas as pd
from pymongo import MongoClient
import pprint


def usage():
    print ("Invalid Options.\n")

    print ("Usage : \n")
    print ("Import trustee to MongoDB")
    print ("./CSVParser.py -i -t <csvtrusteefile> -v <volname> \n")

    print ("Delete trustee collection in MongoDB")
    print ("./CSVParser.py -d -v <volname> ")
    sys.exit()

def purgeCollectionByVolName(volname, collection):
    print ("Delete collection for",volname)
    result = collection.delete_many({ "VOL" : volname})

def insertToDB(rowlist, collection, volname):
    count = 0
    for index, row in rowlist.iterrows():
        count = count + 1
        post = { "VOL" : volname, "Path" : row['Path'], "Rights" : row['RIGHTS'], "TRUSTEE" : row['TRUSTEE']}
        post_id = collection.insert_one(post).inserted_id
        #print (post_id)
        print ("Inserted",count,"rows")




def main(argv):


    importmode = 0
    deletemode = 0
    inputfile = ""

    ### Get Arguments
    try:
        opts, args = getopt.getopt(argv, "idt:v:h", longopts = ["import", "delete", "trustees=", "volname=","help"])
    except getopt.GetoptError:
        usage()
        sys.exit(2)

    for opt, arg in opts:
        if opt in("-h", "--help"):
            usage()
            sys.exit()

        ##Get trustee file
        elif opt in ( '-i', '--import'):
            importmode = 1

        ##Get trustee file
        elif opt in ( '-d', '--delete'):
            deletemode = 1

        ##Get trustee file
        elif opt in ( '-t', '--trustees'):
            inputfile = arg

        ##Get volume name
        elif opt in ( '-v', '--volname'):
            volname = arg

    if ((importmode == 1) and (deletemode == 1)):
        print ("Incompatible options : -i and -d")
        usage()

    if ((importmode == 0) and (deletemode == 0)):
        print ("Error : Specify -i or -d")
        usage()

    if ((importmode == 1) and (inputfile == "")):
        print ("Specify trustee file in import mode")
        usage()


    ### Connect to Database
    client = MongoClient()
    db = client.DGAC

    trustees = db['trustees']
    owners = db['owners']
    attr = db['attr']
    irm = db['irm']

    if (deletemode == 1):
        ### Purge records for volname
        purgeCollectionByVolName(volname, trustees)

    ### Import mode enable
    if (importmode == 1):
        print ("Import",inputfile," in MongoDB for volume",volname)

        ### Purge records for volname
        purgeCollectionByVolName(volname, trustees)
        #purgeCollectionByVolName(volname, owners)
        #purgeCollectionByVolName(volname, attr)
        purgeCollectionByVolName(volname, irm)



        ### Use Latin1 for Netware Trustee file
        with codecs.open(inputfile, encoding='latin1') as csvfile:
            tl = pd.read_csv(inputfile, encoding='latin1')

            tl.sort_values(by='Path')


            ownerrows = tl.loc[tl['TYPE'] == 'OWNER']
            trusteerows = tl.loc[tl['TYPE'] == 'TRUSTEE']
            attrrows = tl.loc[tl['TYPE'] == 'ATTR']
            irmrows = tl.loc[tl['TYPE'] == 'IRM']

            #insertToDB(ownerrows, owners, volname)
            #insertToDB(attrrows, attr, volname)
            insertToDB(irmrows, irm, volname)
            insertToDB(trusteerows, trustees, volname)

            #print (row['Path'],row['RIGHTS'],row['TRUSTEE'])


if __name__ == "__main__":
    main(sys.argv[1:])
