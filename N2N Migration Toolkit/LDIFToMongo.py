#!/usr/bin/env python3

import sys
import argparse
from ldif3 import LDIFParser
from pprint import pprint
import pandas as pd
from pymongo import MongoClient


def insertLineToDB(post, collection):
    post_id = collection.update_one(post, { '$set' : post }, upsert=True)

def purgeUserBase(volname, collection):
    print ("Delete collection for",volname)
    result = collection.delete_many()

def main(self):

    parser = argparse.ArgumentParser()

    parser.add_argument("-f","--ldiffile", type=str, dest='ldiffile', help="LDIF File")
    parser.add_argument("-b","--database", type=str, dest='dbname', help="DB Name")
    parser.add_argument("--inject", help="Inject Data", action="store_true")
    parser.add_argument("--export", help="Export Data", action="store_true")
    parser.add_argument("--user", help="User Import", action="store_true")
    parser.add_argument("--group", help="Group Import", action="store_true")


    if len(sys.argv)==1:
        parser.print_help()
        sys.exit(1)
    args = parser.parse_args()


    ### Connect to Database
    client = MongoClient()
    db = client[args.dbname]
    UserCollection = db['Users']
    GroupCollection = db['Groups']

    if (args.inject):
        if (args.user):
            ldifparser = LDIFParser(open(args.ldiffile, 'rb'))
            user = {}
            for dn, entry in ldifparser.parse():
                #print ('got entry record : %s' % dn)
                #print (dn)
                cn = ""
                mail = ""
                uid = ""

                for element in entry.items():
                    ### Get the CN
                    if (element[0] in "cn"):
                        cn = element[1][0]

                    ### Get the mail
                    if (element[0] in "mail"):
                        mail = element[1][0]

                    ### Get the UID
                    if (element[0] in "uid"):
                        uid = element[1][0]

                if (cn != mail):
                    #print ({ 'cn' : cn, 'mail' : mail, 'uid' : uid})
                    insertLineToDB({ 'dn' : dn, 'cn' : cn, 'mail' : mail, 'uid' : uid}, UserCollection)
                else:
                    print ("Found "+cn+" in "+mail+"for :"+dn)

        if (args.group):
            ldifparser = LDIFParser(open(args.ldiffile, 'rb'))
            for dn, entry in ldifparser.parse():
                #print ('got entry record : %s' % dn)
                cn = ""
                member = []


                for element in entry.items():
                    ### Get the CN
                    if (element[0] in "cn"):
                        cn = element[1][0]

                    ### Get the mail
                    if (element[0] in "member"):
#                        print (element[1])
                        member.append(element[1])

                print ({ 'cn' : cn, 'member' : member})
                insertLineToDB({ 'dn' : dn, 'cn' : cn, 'member' : member}, GroupCollection)


    #insertLineToDB(user, UserCollection)

    if (args.export):
        pd.DataFrame(list(UserCollection.find())).to_csv("userexport.csv")



if __name__ == "__main__":
    main(sys.argv[1:])
