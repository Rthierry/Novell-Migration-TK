#!/usr/bin/env python3

import sys
import getopt
import pprint
from pymongo import MongoClient
import argparse
from classes.NSSVolume import NSSVolume
import pandas as pd

def main(argv):

    parser = argparse.ArgumentParser()
    parser.add_argument("-b","--database", type=str, dest='dbname', help="DB Name")
    parser.add_argument("-v","--volname", type=str, dest='volname', help="Volume Name")
    parser.add_argument("--generateRights", help="Generate rights", action="store_true")
    parser.add_argument("-e","--exportToCSV", help="Export rights to CSV", action="store_true")





    if len(sys.argv)==1:
        parser.print_help()
        sys.exit(1)
    args = parser.parse_args()

    if (args.dbname == None):
        print ("DB name not defined. -b or --database mandatory")
        parser.print_help()
        sys.exit(1)


    volume = NSSVolume(args.volname, args.dbname)

    if (args.generateRights):
        volume.generateRights()

    if (args.exportToCSV):
        print ("Export to CSV")
        nssExport = args.volname+"-nss.csv"
        ntfsExport = args.volname+"-ntfs.csv"
        traverseFolderCollectionExport = args.volname+"-travFolder.csv"
        traverseGroupMembershipExport = args.volname+"-travGrpMembership.csv"

        ntfsDataFrame = pd.DataFrame(list(volume.ntfsAceList))
        nssDataFrame = pd.DataFrame(list(volume.aceList))
        traverseFolderCollectionDataFrame = pd.DataFrame(list(volume.traverseFolderList))
        traverseGroupMembershipDataFrame = pd.DataFrame(list(volume.traverseGroupMembershipList))


        ntfsDataFrame.to_csv(ntfsExport)
        nssDataFrame.to_csv(nssExport)
        traverseGroupMembershipDataFrame.to_csv(traverseGroupMembershipExport)

        #traverseFolderCollectionDataFrame.to_csv(traverseFolderCollectionDataFrame)
        print ("NSS Permission : "+nssExport)
        print ("NTFS Permission : "+ntfsExport)
        print ("Traverse Group Membership : "+traverseGroupMembershipExport)










    ### Generate CSV file













if __name__ == "__main__":
    main(sys.argv[1:])
