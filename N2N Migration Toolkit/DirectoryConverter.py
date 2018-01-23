#!/usr/bin/env python3

import sys
import getopt
import pprint
from pymongo import MongoClient
import argparse
import pandas as pd
from classes.NSSVolume import NSSVolume
from classes.DirectoryDB import DirectoryDB



def main(self):

    parser = argparse.ArgumentParser()
    parser.add_argument("-b","--database", type=str, dest='dbname', help="DB Name")
    parser.add_argument("-l","--logfile", type=str, dest='logfile', help="Volume Name")
    parser.add_argument("--verbose", help="Verbose Mode", action="store_true")
    parser.add_argument("--exportToCSV", help="Export rights to CSV", action="store_true")
    parser.add_argument("--showUsers", help="Print Users", action="store_true")
    parser.add_argument("--showGroups", help="Print Groups", action="store_true")
    parser.add_argument("--generateMemberList", help="Generate Member List from user and group", action="store_true")


    if len(sys.argv)==1:
        parser.print_help()
        sys.exit(1)
    args = parser.parse_args()

    if (args.dbname == None):
        print ("DB name not defined. -b or --database mandatory")
        parser.print_help()
        sys.exit(1)

    directory = DirectoryDB(args.dbname, args.verbose)

    if (args.exportToCSV):
        print ("Export to CSV")
        DirectoryDB.exportToCSV()

    if (args.showUsers):
        for row in DirectoryDB.UserList:
            print (row)

    if (args.showGroups):
        for row in DirectoryDB.GroupList:
            print (row)

    if (args.generateMemberList):
        directory.generateMemberList()


if __name__ == "__main__":
    main(sys.argv[1:])
