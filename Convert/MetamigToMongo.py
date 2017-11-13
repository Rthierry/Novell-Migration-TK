#!/usr/bin/env python3

import sys
import getopt
from lxml import etree
from pymongo import MongoClient
import argparse


def purgeCollectionByVolName(volname, collection):
    print ("Delete collection for",volname)
    result = collection.delete_many({ "Volume" : volname})

def insertToDB(rowlist, collection, volname):
    count = 0
    for row in rowlist:
        count = count + 1
        post = { "Volume" : volname, "Path" : row['path'], "Rights" : row['rights'], "Trustee" : row['name']}
        post_id = collection.insert_one(post).inserted_id
        #print (post_id)
        print ("Inserted "+str(count)+" rows into for "+volname)

def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("-i","--inject", help="Import Mode", action="store_true")
    parser.add_argument("-d","--delete", help="Delete Mode", action="store_true")
    parser.add_argument("-t","--trustees", type=str, dest='inputfile', help="Fichier trustees metamig")
    parser.add_argument("-v","--volname", type=str, dest='volname', help="Volume Name")
    parser.add_argument("-b","--database", type=str, dest='dbname', help="Database Name")

    if len(sys.argv)==1:
        parser.print_help()
        sys.exit(1)
    args = parser.parse_args()

    if ((args.inject) and (args.inputfile == "")):
        print ("Specify trustee file in import mode")
        parser.print_help()
        sys.exit(1)

    if (args.volname == None):
        print ("Volume name not defined. -v mandatory")
        parser.print_help()
        sys.exit(1)

    if (args.dbname == None):
        print ("DB name not defined. -b or --database mandatory")
        parser.print_help()
        sys.exit(1)

    if ((args.inject) and (args.delete)):
        print ("Incompatible argument. Can't inject and delete at the same time")
        sys.exit(1)



    ### Connect to Database
    client = MongoClient()

    ### Change DB Name here
    db = client[args.dbname]

    NSSTrusteesCollection = db['NSSTrustees']
    irm = db['NSSIrf']

    if (args.delete):
        print (args.delete)
        ### Purge records for volname
        purgeCollectionByVolName(args.volname, NSSTrusteesCollection)

    ### Import mode enable
    if (args.inject):
        print ("Import",args.inputfile," in MongoDB for volume",args.volname)
        purgeCollectionByVolName(args.volname, NSSTrusteesCollection)

        ### Import XML file
        tree = etree.parse(args.inputfile)

        trusteerows = []

        for filenode in tree.xpath("trusteeInfo/file"):
            for path in filenode.xpath("path"):
                trusteepath = path.text
            for trustee in filenode.xpath("trustee"):
                for trusteename in trustee.xpath("name"):
                    name = trusteename.text
                for trusteerights in trustee.xpath("rights"):
                    rights = trusteerights.get("value")

                trusteerow = { 'path' : trusteepath , 'name' : name , 'rights' : rights }
                trusteerows.append(trusteerow)

        insertToDB(trusteerows, NSSTrusteesCollection, args.volname)



if __name__ == "__main__":
    main(sys.argv[1:])
