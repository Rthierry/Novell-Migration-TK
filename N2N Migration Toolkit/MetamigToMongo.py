#!/usr/bin/env python3

import sys
import getopt
from lxml import etree
from pymongo import MongoClient
import argparse





def insertLineToDB(post, collection):
    post_id = collection.update_one( post, { '$set' : post }, upsert=True)

def updateLineInDB(match, post, collection):
    post_id = collection.update_one(match, { "$set" : post}, upsert=False)


def purgeCollectionByVolName(volname, collection):
    print ("Delete collection for",volname)
    result = collection.delete_many({ "Volume" : volname})



def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("-i","--inject", help="Import Mode", action="store_true")
    parser.add_argument("--test", help="Test Mode for dev, not to be used", action="store_true")
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
    NSSQuotasCollection = db['NSSQuotas']
    IRFCollection = db['NSSIrf']
    NSSTrusteesVersionCollection = db['NSSTrusteesVersion']


    ### Test mode, not to be used
    if (args.test):
        oldversion = NSSTrusteesVersionCollection.find_one({'Status' : 'Current', 'Volume' : args.volname })
        if ( oldversion == None ):
            post = { 'Status' : 'Current', 'Version' : 1}
            insertLineToDB (post, NSSTrusteesVersionCollection)
        else:
            print ("Last version was "+ str(oldversion['Version']))
            match = { 'Status' : 'Current', 'Volume' : args.volname }
            updateLineInDB(match, {'Status' : 'Old'}, NSSTrusteesVersionCollection)

            newversion = int(oldversion['Version']) + 1
            post = { 'Status' : 'Current', 'Version' : newversion, 'Volume' : args.volname  }
            insertLineToDB(post, NSSTrusteesVersionCollection)



    if (args.delete):
        print (args.delete)
        ### Purge records for volname
        purgeCollectionByVolName(args.volname, NSSTrusteesCollection)
        purgeCollectionByVolName(args.volname, IRFCollection)
        purgeCollectionByVolName(args.volname, NSSQuotasCollection)

    ### Import mode enable
    if (args.inject):

#        purgeCollectionByVolName(args.volname, NSSTrusteesCollection)

        oldversion = NSSTrusteesVersionCollection.find_one({'Status' : 'Current', 'Volume' : args.volname })
        if ( oldversion == None ):
            post = { 'Status' : 'Current', 'Version' : 1, 'Volume' : args.volname }
            insertLineToDB (post, NSSTrusteesVersionCollection)
            newversion = 1
            print ("Updating version number to "+str(newversion))
        else:
            print ("Last version was "+ str(oldversion['Version']))
            newversion = int(oldversion['Version']) + 1
            match = { 'Status' : 'Current' , 'Volume' : args.volname  }
            updateLineInDB(match, {'Status' : 'Old'}, NSSTrusteesVersionCollection)

            post = { 'Status' : 'Current', 'Version' : newversion, 'Volume' : args.volname  }
            print ("Updating version number to "+str(newversion))
            insertLineToDB(post, NSSTrusteesVersionCollection)




        print ("Import",args.inputfile," in MongoDB for volume",args.volname)
        lines = []
        with open(args.inputfile) as infile, open (args.inputfile+"-charfixed",'w') as outfile:
            for line in infile:
                line = line.replace('&', '&amp;')
                outfile.write(line)

        ### Import XML file
        tree = etree.parse(args.inputfile+"-charfixed")

        trusteerows = []

        trusteecount = 0
        irfcount = 0
        quotaCount = 0

        for filenode in tree.xpath("trusteeInfo/file"):


            for path in filenode.xpath("path"):
                trusteepath = path.text
            for trustee in filenode.xpath("trustee"):
                for trusteename in trustee.xpath("name"):
                    name = trusteename.text

                for trusteeid in trustee.xpath("id"):
                    tid = trusteeid.text

                for trusteerights in trustee.xpath("rights"):
                    rights = trusteerights.get("value")
                    trusteerow = { 'Volume' : args.volname, 'path' : trusteepath , 'name' : name , 'rights' : rights, 'Version' : newversion, 'TID' : tid }
                    trusteecount = trusteecount + 1
                    insertLineToDB(trusteerow, NSSTrusteesCollection)

            for irf in filenode.xpath("inheritedRightsFilter"):
                irfentry = irf.get("value")
                irfrow = {'Volume' : args.volname, 'Path' : trusteepath, 'Filter' : irfentry, 'Version' : newversion}
                insertLineToDB(irfrow, IRFCollection)
                irfcount = irfcount + 1

        quotarows = []

        for directory in tree.xpath("dirInfo/directory"):
            for path in directory.xpath("path"):
                currentPath = path.text

            for spaceUsed in directory.xpath("quotaAmount"):
                if ((spaceUsed.text != "9223372036854775807")):
                    currentQuotas = spaceUsed.text
                    quotarow = { 'Volume' : args.volname, 'path' : currentPath, 'quota' : currentQuotas, 'Version' : newversion}
                    insertLineToDB(quotarow,NSSQuotasCollection)
                    quotaCount = quotaCount + 1

        print ("\nTotal : ")
        print (str(trusteecount)+" trustees")
        print (str(irfcount)+" irfs")
        print (str(quotaCount)+" quotas")


        print ("\nTo show result, run :  ")
        print ("\t./NSSConverter.py -b "+args.dbname+" -v "+args.volname)
        print ("\twith --showQuotas, --showIrfs or --showNSSTrustees option\n")







if __name__ == "__main__":
    main(sys.argv[1:])
