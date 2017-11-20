#!/usr/bin/env python3

import sys
import getopt
import pprint
from pymongo import MongoClient
import argparse
from classes.NSSVolume import NSSVolume
import pandas as pd


def main(self):

    parser = argparse.ArgumentParser()
    parser.add_argument("-b","--database", type=str, dest='dbname', help="DB Name")
    parser.add_argument("-v","--volname", type=str, dest='volname', help="Volume Name")
    parser.add_argument("-l","--logfile", type=str, dest='logfile', help="Volume Name")
    parser.add_argument("--generateRights", help="Generate rights", action="store_true")
    parser.add_argument("--verbose", help="Generate rights", action="store_true")
    parser.add_argument("--exportToCSV", help="Export rights to CSV", action="store_true")
    parser.add_argument("--showIrfs", help="Print Irfs", action="store_true")
    parser.add_argument("--showQuotas", help="Print Quotas", action="store_true")
    parser.add_argument("--showNSSTrustees", help="Print NSS Trustees", action="store_true")
    parser.add_argument("--showNTFSAce", help="Print NTFS Trustees", action="store_true")


    if len(sys.argv)==1:
        parser.print_help()
        sys.exit(1)
    args = parser.parse_args()

    if (args.dbname == None):
        print ("DB name not defined. -b or --database mandatory")
        parser.print_help()
        sys.exit(1)

    volume = NSSVolume(args.volname, args.dbname, args.verbose)

#    if (args.verbose):
#        volume.verbose = 1

    if (args.generateRights):
        volume.generateRights()

    if (args.exportToCSV):
        print ("Export to CSV")
        volume.exportToCSV()

    if (args.showNSSTrustees):
        for row in volume.aceList:
            print (row)

    if (args.showNTFSAce):
        for row in volume.ntfsAceList:
            print (row)

    if (args.showQuotas):
        for row in volume.NSSQuotasList:
            print (row)

    if (args.showIrfs):
        for row in volume.NSSIRFList:
            print (row)

if __name__ == "__main__":
    main(sys.argv[1:])
