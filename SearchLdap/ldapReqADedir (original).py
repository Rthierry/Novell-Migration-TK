#!/usr/bin/env python
# -*- coding: utf8 -*-
# @Author: Thierry Rangeard <Gandalf>
# @Date:   04-Oct-2016
# @Email:  trangeard@net-online.fr
# @Project: Utilitaire de lecture ldap
# @Last modified by:   Gandalf
# @Last modified time: 28-Aug-2017
from ldap3 import Server, Connection, ALL_ATTRIBUTES, SCHEMA, SUBTREE, AUTO_BIND_NO_TLS, set_config_parameter
import argparse
import ssl
import json
import csv
parser = argparse.ArgumentParser()
parser.add_argument("servername", type=str, help=" -> serverldap")
parser.add_argument("username", type=str, help=" -> username")
parser.add_argument("password", type=str, help=" -> password")
parser.add_argument("dnbase", type=str, help=" -> dnbase")

# Accept Self-Sign Certificates
# ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)
#server = Server('10.134.2.43' ,port=389, use_ssl=False, get_info=ALL_ATTRIBUTES)
server = Server('10.4.1.47' ,port=389, use_ssl=False, get_info=ALL_ATTRIBUTES)
set_config_parameter('DEFAULT_CLIENT_ENCODING', 'utf8')
BaseAD = "ou=grp_sces,ou=groupes,dc=adchpg,dc=chpg,dc=mc"
BaseeDir = "ou=grp_partages,O=chpg"
Scope = 'SUBTREE'
FilterAD = "(&(objectClass=Group)(!(objectClass=computer)))"
FiltereDir = "(&(objectClass=Group))"
AttrsAD = ['samAccountName','dn','member','cn']
AttrseDir = ['dn','member','cn']
#conn = Connection(server, 'cn=Netonline,ou=Externes,ou=Utilisateurs,dc=adchpg,dc=chpg,dc=mc', 'Netonline@26', auto_bind=True)
#conn.search(search_base=BaseAD, search_filter=FilterAD, search_scope=Scope, attributes=AttrsAD )

conn = Connection(server, 'cn=netonline,ou=presta,ou=ext,o=chpg', 'Netonline@26', auto_bind=True)
conn.search(search_base=BaseeDir, search_filter=FiltereDir, search_scope=Scope, attributes=AttrseDir)

trustee_data = open('listmembreeDir.csv', 'w')
#trustee_data = open('listmembreAD.csv', 'w')
csvwriter = csv.writer(trustee_data)
#trustee_data_head = ['GroupeAD','samAccountName','nombre de membres',]
trustee_data_head = ['GroupeeDir', 'nombre de membres',]
csvwriter.writerow(trustee_data_head)
for row in conn.entries:
    print(row.cn[0])
    print(row.member.value)
    #print(row.samAccountName)
    line = []
    groupname = row.cn[0]
    print (groupname)
    line.append(groupname)
    #sam = (row.samAccountName)
    #print(sam)
    #line.append(sam)
    if len(row.member.values or ()) == 0:
        membres = 0
    else:
        membres = len(row.member.value)
    line.append(membres)
    print(membres)
    csvwriter.writerow(line)
trustee_data.close()
