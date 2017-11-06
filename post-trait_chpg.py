# @Author: Thierry Rangeard <Gandalf>
# @Date:   29-Aug-2017
# @Email:  trangeard@net-online.fr
# @Project: Utilitaire de traitement fichier trustees pour chpg separation en colonne user - group
# @Last modified by:   Gandalf
# @Last modified time: 29-Aug-2017
import unicodedata
import re
import sys
import csv
import argparse

parser = argparse.ArgumentParser()
parser.add_argument("-i", type=str, dest='input_file', help=" -> Fichier trustees_xxx_trustee.csv")
if len(sys.argv)==1:
    parser.print_help()
    sys.exit(1)
args = parser.parse_args()

def Trait_1(csv_file):
    with open( csv_file, 'rt') as f:
        csvreader = csv.reader(f)
        trustee_data = open(args.input_file.strip('.csv')+"_trait1.csv", 'w')
        csvwriter = csv.writer(trustee_data)
        trustee_data_head = ['chemin', 'ayant-droits-usr', 'ayant-droits-grp','droits']
        csvwriter.writerow(trustee_data_head)
        for row in csvreader:
                s = re.search('GRP',row[1])
                line = []
                if s:
                    chemin = row[0]
                    line.append(chemin)
                    usr = ""
                    line.append(usr)
                    grp = row[1]
                    line.append(grp)
                    droits= row[2]
                    line.append(droits)
                    print (chemin + " " + usr + " " + grp + " "+ droits)
                    csvwriter.writerow(line)
                else:
                    chemin = row[0]
                    line.append(chemin)
                    usr = row[1]
                    line.append(usr)
                    grp = ""
                    line.append(grp)
                    droits = row[2]
                    line.append(droits)
                    csvwriter.writerow(line)

        ##    for element in member.findall('path'):
        #        print ("path :"),chemin
        ##            fichier = []
        #            fichier.append(chemin)
        #            ayant_droits = trustees.find('name').text
        ####        droits = trustees.find('rights').get('value')
        #            print ("droits:"),droits
        #            fichier.append(droits)
        #            csvwriter.writerow(fichier)
        trustee_data.close()
    return()
if __name__ == "__main__":
    Trait_1(args.input_file)
