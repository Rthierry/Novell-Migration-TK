#!/usr/bin/python
# -*- coding: latin-1 -*-
# @Author: Thierry Rangeard <Gandalf>
# @Date:   02-Oct-2016
# @Email:  trangeard@net-online.fr
# @Project: Utilitaire import nss - pandas
# @Last modified by:   Gandalf
# @Last modified time: 02-Oct-2016
import pandas as pd
import sys
import getopt
reload(sys)
sys.setdefaultencoding("utf8")


def main(argv):
    inputfile = ''
    try:
        opts, args = getopt.getopt(argv, "hi:", ["ifile="])
    except getopt.GetoptError:
        print 'nss2csv.py -i <inputfile.xml>'
        sys.exit(2)
        for opt, arg in opts:
            if opt == '-h':
                print 'nss2csv.py -i <inputfile.xml> deux fichiers en sortie _trustee.csv et _quota.csv'
                sys.exit()
            elif opt in ("-i", "--ifile"):
                inputfile = arg
                print 'Le fichier traité est :', inputfile
    return()

if __name__ == "__main__":
    df = pd.read_csv(sys.argv[1])
    print list(df.groupby(['chemin', 'ayant-droits']))
