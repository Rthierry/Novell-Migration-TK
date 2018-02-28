#!/usr/bin/env python3

import sys
import getopt
import re
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

def initiateNewVersion(volname, collection):

    oldversion = collection.find_one({'Status' : 'Current', 'Volume' : volname })
    if ( oldversion == None ):
        post = { 'Status' : 'Current', 'Version' : 1, 'Volume' : volname }
        insertLineToDB (post, collection)
        newversion = 1
        print ("Updating version number to "+str(newversion))
        return newversion
    else:
        print ("Last version was "+ str(oldversion['Version']))
        newversion = int(oldversion['Version']) + 1
        match = { 'Status' : 'Current' , 'Volume' : volname  }
        updateLineInDB(match, {'Status' : 'Old'}, collection)

        post = { 'Status' : 'Current', 'Version' : newversion, 'Volume' : volname  }
        print ("Updating version number to "+str(newversion))
        insertLineToDB(post, collection)
        return newversion
    


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("-i","--inject", help="Import Mode", action="store_true")
    parser.add_argument("--test", help="Test Mode for dev, not to be used", action="store_true")
    parser.add_argument("-d","--delete", help="Delete Mode", action="store_true")
    parser.add_argument("-t","--trustees", type=str, dest='inputfile', help="Fichier trustees metamig")
    parser.add_argument("-v","--volname", type=str, dest='volname', help="Volume Name")
    parser.add_argument("-b","--database", type=str, dest='dbname', help="Database Name")
    parser.add_argument("--metamig", help="Metamig input file", action="store_true" )
    parser.add_argument("--trusteesdb", help="Trustees DB input file", action="store_true" )

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

    if (args.trusteesdb & args.metamig):
        print ("It's both a --metamig AND a --trusteedb file ? Stop the BS.")
        sys.exit(1)

    if ( (args.trusteesdb | args.metamig) != True ):
        print ("Is it a --metamig or a --trusteeb file ? ")
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
        print ("test")



    if (args.delete):
        print (args.delete)
        ### Purge records for volname
        purgeCollectionByVolName(args.volname, NSSTrusteesCollection)
        purgeCollectionByVolName(args.volname, IRFCollection)
        purgeCollectionByVolName(args.volname, NSSQuotasCollection)


    


    ##############################################
    ### Import mode enable using Metamig File  ###
    ##############################################
    if (args.inject & args.metamig):

        newversion = initiateNewVersion(args.volname, NSSTrusteesVersionCollection)

        print ("Import",args.inputfile," in MongoDB for volume",args.volname)

        with open(args.inputfile) as infile, open (args.inputfile+"-charfixed",'w') as outfile:
            for line in infile:
                line = line.replace('&', '&amp;')
                outfile.write(line)

        ### Import XML file
        tree = etree.parse(args.inputfile+"-charfixed")

        trusteecount = 0
        irfcount = 0
        quotaCount = 0

        for filenode in tree.xpath("trusteeInfo/file"):
            for path in filenode.xpath("path"):
                trusteepath = path.text
            for trustee in filenode.xpath("trustee"):
                for trusteename in trustee.xpath("name"):
                    name = trusteename.text

                    #print ("Old name : "+name)
                    name = re.sub("\.T=.*","",name)                    
                    name = re.sub("\.[^=]*=",".",name)                    
                    #print("New name : "+name)

                for trusteerights in trustee.xpath("rights"):
                    rights = trusteerights.get("value")
                    trusteerow = { 'Volume' : args.volname, 'path' : trusteepath , 'name' : name , 'rights' : rights, 'Version' : newversion}
                    trusteecount = trusteecount + 1
                    insertLineToDB(trusteerow, NSSTrusteesCollection)

            for irf in filenode.xpath("inheritedRightsFilter"):
                irfentry = irf.get("value")
                irfrow = {'Volume' : args.volname, 'Path' : trusteepath, 'Filter' : irfentry, 'Version' : newversion}
                insertLineToDB(irfrow, IRFCollection)
                irfcount = irfcount + 1


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
    
    


    ########################################################
    ### Import mode enable using trustees_database File  ###
    ########################################################
    if (args.inject & args.trusteesdb):
        
        newversion = initiateNewVersion(args.volname, NSSTrusteesVersionCollection)

        print ("Import",args.inputfile," in MongoDB for volume",args.volname)
        with open(args.inputfile) as infile, open (args.inputfile+"-charfixed",'w') as outfile:
            for line in infile:
                line = line.replace('&', '&amp;')
                outfile.write(line)

        ### Import XML file    
        tree = etree.parse(args.inputfile+"-charfixed")

        trusteecount = 0
        irfcount = 0
        quotaCount = 0
        
        for trustee in tree.xpath("trustee"):
            ### Get path in trustee tag
            trusteepath = trustee.get("path")

            ### Get name in name tag
            for trusteename in trustee.xpath("name"):
                name = trusteename.text

            ### Get right in rights tab
            for trusteerights in trustee.xpath("rights"):
                if (trusteerights.text != None ):
                    rights = trusteerights.text.lower()


            ### Build JSON post
            trusteerow = { 'Volume' : args.volname, 'path' : trusteepath , 'name' : name , 'rights' : rights, 'Version' : newversion}                    
            trusteecount = trusteecount + 1

            ### Post to Mongo
            insertLineToDB(trusteerow, NSSTrusteesCollection)


        for irf in tree.xpath("inheritedRightsFilter"):
            irfpath = trusteepath.get("path")

             ### Get right in rights tab
            for trusteerights in trustee.xpath("rights"):
                    rights = trusteerights.text

            irfentry = rights.text
            irfrow = {'Volume' : args.volname, 'Path' : irfpath, 'Filter' : rights, 'Version' : newversion}
            insertLineToDB(irfrow, IRFCollection)
            irfcount = irfcount + 1

        print ("\nTotal : ")
        print (str(trusteecount)+" trustees")
        print (str(irfcount)+" irfs")

        print ("\nTo show result, run :  ")
        print ("\t./NSSConverter.py -b "+args.dbname+" -v "+args.volname)
        print ("\twith --showIrfs or --showNSSTrustees option\n")


if __name__ == "__main__":
    main(sys.argv[1:])
