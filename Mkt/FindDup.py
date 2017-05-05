# @Author: Thierry Rangeard <Gandalf>
# @Date:   04-May-2017
# @Email:  trangeard@net-online.fr
# @Project: Utilitaire de recherche Homonyme
# @Last modified by:   Gandalf
# @Last modified time: 04-May-2017
#!/usr/bin/python
# -*- coding: latin-1 -*-

import unicodedata
import sys
import argparse
import pandas as pd
reload(sys)
sys.setdefaultencoding("utf8")
parser = argparse.ArgumentParser()
parser.add_argument("-i1", type=str, dest='input_file1', help=" -> Fichier un AD")
parser.add_argument("-i2", type=str, dest='input_file2', help=" -> Fichier deux GW")
parser.add_argument("-i3", type=str, dest='input_dom', help=" -> Domaine a supprimer")
if len(sys.argv)==1:
    parser.print_help()
    sys.exit(1)
args = parser.parse_args()

if __name__ == "__main__":
    fichier_un = args.input_file1
    fichier_deux = args.input_file2
    domain = args.input_dom
    df1 = pd.read_csv(fichier_un,dtype=str);
    df2 = pd.read_csv(fichier_deux,dtype=str);
    print (df2.destinationEmail.str.strip(domain))
    print (df1.Alias)
    dup = df1.Alias.isin(df2.destinationEmail.str.strip(domain))
    print (dup)
