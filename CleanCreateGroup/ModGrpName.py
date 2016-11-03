#!/usr/bin/python
#-*- coding: utf-8 -*-
# @Author: Thierry Rangeard <Gandalf>
# @Date:   03-Nov-2016
# @Email:  trangeard@net-online.fr
# @Project: Utilitaire de reecriture des groupes
# @Last modified by:   Gandalf
# @Last modified time: 03-Nov-2016
# @Input file : volumename.acl
# @Output file : volumename-gprmod.acl

import sys, getopt
reload(sys);
sys.setdefaultencoding("utf8")
import csv
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("input_aclfile", type=str, help=" -> Fichier trustee XXX.xml-acl.csv")
parser.add_argument("input_grpfile", type=str, help=" -> Fichier groupe importAD_Group.csv")

args = parser.parse_args()


def FindGRP(input_aclfile, input_grpfile):
    with open(input_aclfile, 'rb') as csvacllist:
        # open file as dictionnary the columns headers:values
        csvreaderacl = csv.DictReader(csvacllist)
        # open file with all the groups into the first row[0]
        with open(input_grpfile, 'rb') as csvgrplist:
            # open a new file for writing the resulting match elements
            with open(input_aclfile.strip('.xml-acl.csv')+"_corrected.xml-acl.csv", 'wb') as csvgrpoutput:
                # Use the same field names for the output file.
                writeracl = csv.DictWriter(csvgrpoutput, csvreaderacl.fieldnames)
                writeracl.writeheader()
                csvreaderrowgrp = csv.reader(csvgrplist)
                # list built from the first row
                rows_grp_col2 = [row[0] for row in csvreaderrowgrp]
                linenum = 0
                for item in csvreaderacl:
                    # looking for the key 'uid'
                    if item.get('uid') not in rows_grp_col2:
                        linenum = linenum + 1
                        print("NB droits utilisateur trouvé : " + str(linenum) + " " +item.get('uid'))
                        # writing
                        writeracl.writerow(item)
                    else:
                        # if match get the value with the 'uid' key
                        item['uid'] = "GG_"+item.get('uid')
                        print ("Correspondance GRP trouvé : " + item['uid'])
                        # writing the row to the new file
                        writeracl.writerow(item)
    return()
if __name__ == "__main__":
    aclfile = args.input_aclfile
    groupefile = args.input_grpfile
    FindGRP(aclfile, groupefile)
