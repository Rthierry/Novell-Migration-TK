#!/usr/bin/env python3

import sys
import argparse
from ldif3 import LDIFParser
from pprint import pprint
import pandas as pd
from pymongo import MongoClient

from classes.NSSVolume import NSSVolume
from classes.DirectoryDB import DirectoryDB


def insertLineToDB(post, collection):
    post_id = collection.update_one(post, { '$set' : post }, upsert=True)

def purgeUserBase(volname, collection):
    print ("Delete collection for",volname)
    result = collection.delete_many()

def main(self):

    parser = argparse.ArgumentParser()

    parser.add_argument("-b","--database", type=str, dest='dbname', help="DB Name")
    parser.add_argument("-v","--volname", type=str, dest='volname', help="Volume Name")
    parser.add_argument("-u","--user", type=str, dest='user', help="User reporting")
    parser.add_argument("-g","--group", type=str, dest='group', help="Group reporting")
    parser.add_argument("--diff", help="Diff Mode", action="store_true")
    parser.add_argument("--newdiff", help="Diff Mode v2", action="store_true")
    parser.add_argument("--pre", type=str, dest='pre', help="Used in differential mode, define initial version")
    parser.add_argument("--post", type=str, dest='post', help="Used in differential mode, define target version")
    parser.add_argument("--verbose", help="Verbose Mode", action="store_true")


    if len(sys.argv)==1:
        parser.print_help()
        sys.exit(1)
    args = parser.parse_args()


    ### Connect to Database
    client = MongoClient()
    db = client[args.dbname]
    UserCollection = db['Users']
    GroupCollection = db['Groups']


    if (args.dbname == None):
        print ("DB name not defined. -b or --database mandatory")
        parser.print_help()
        sys.exit(1)

    if (args.volname == None):
        print ("Volume name not defined. -v or --volume mandatory")
        parser.print_help()
        sys.exit(1)

    directory = DirectoryDB(args.dbname, args.verbose)
    volume = NSSVolume(args.volname, args.dbname, args.verbose)

    if (args.user):
        permissions = directory.getUserPermissionsOnVol(args.user, args.volname)
        for element in permissions:
            #print ("Looking for "+element['groupid']+" in database.")
            for ace in volume.NTFSAceCollection.find({'SAMAccountName' : element['groupid'], 'Volume' : args.volname}):
                print ("GROUP ACE --- "+ace['Path']+" : From "+element['groupid']+" with "+ace['Rights'])

        for ace in volume.NTFSAceCollection.find({'SAMAccountName' : args.user, 'Volume' : args.volname}):
            print ("USER ACE --- "+ace['Path']+" : "+ace['Rights'])


    if (args.diff):
        volume = NSSVolume(args.volname, args.dbname, args.verbose)
        volume.showDifferences(args.pre, args.post)
    
if __name__ == "__main__":
    main(sys.argv[1:])
