#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Author: Thierry Rangeard <Gandalf>
# @Date:   04-Nov-2016
# @Email:  trangeard@net-online.fr
# @Project: Utilitaire de verification des comptes
# @Last modified by:   Gandalf
# @Last modified time: 04-Nov-2016
# Les fichiers doivent contenir en col[1] les utilisateurs
# GETclean formate les fichiers

import csv
import argparse
import sys
import re
reload(sys)
sys.setdefaultencoding("utf8")

parser = argparse.ArgumentParser()
parser.add_argument("input_user1", type=str, help=" -> Fichier user 1 ")
parser.add_argument("input_user2", type=str, help=" -> Fichier user 2 ")

args = parser.parse_args()


def  GETclean(input_file, output_file):
    ldapgetcn = re.compile("cn=(.*?),.*", re.IGNORECASE)
    list0 = []
    with open(input_file, 'r') as i:
        content = i.readlines()
        with open(output_file, 'w') as csvoutput:
            writer = csv.writer(csvoutput, lineterminator='\n')
            for line in content:
                list0 = re.findall(ldapgetcn, str(line))
                writer.writerow(list0)
    print('Nettoyage du fichier')
    return()


def  CompUser(input_user1, input_user2):
    with open(input_user1, 'rb') as fileuser1:
        # open file as dictionnary the columns headers:values
        csvuser1 = csv.DictReader(fileuser1)
        # open file with all the groups into the first row[0]
        with open(input_user2, 'rb') as fileuser2:
            csvreaderuser2 = csv.reader(fileuser2)
            # open a new file for writing the resulting match elements
            with open('usernotmatch.csv', 'wb') as csvnotmatch:
                writeracl = csv.DictWriter(csvnotmatch, csvuser1.fieldnames)
                # Use the same field names for the output file.
                writeracl.writeheader()
                # list built from the first row
                rows_user2 = [row[0] for row in csvreaderuser2]
                print rows_user2
                linenum = 0
                for item in csvuser1:
                    # looking for the key 'uid'
                    if item.get('Users') in rows_user2:
                        linenum = linenum + 1
                        # print("Correspondance trouvé : " + str(linenum) + " " + item.get('Users'))
                        # writing
                    else:
                        # if match get the value with the 'uid' key
                        print ("Différence USER trouvé entre edir: " + item['Users'] + " et User AD")
                        # writing the row to the new file
                        print(item)
                        writeracl.writerow(item)
    return()
if __name__ == "__main__":
    useredir = args.input_user1
    userad = args.input_user2
    CompUser(useredir, userad)
    # GETclean(useredir, "useronecl.csv")
