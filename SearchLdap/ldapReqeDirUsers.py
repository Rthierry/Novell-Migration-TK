# @Author: Thierry Rangeard <Gandalf>
# @Date:   30-Aug-2017
# @Email:  trangeard@net-online.fr
# @Project: Utilitaire de recherche Attributs User.
# @Last modified by:   Gandalf
# @Last modified time: 30-Aug-2017

from ldap3 import Server, Connection, ALL_ATTRIBUTES, SCHEMA, SUBTREE, AUTO_BIND_NO_TLS, set_config_parameter
import argparse
import ssl
import time
import csv
import calendar

parser = argparse.ArgumentParser()
parser.add_argument("servername", type=str, help=" -> serverldap")
parser.add_argument("username", type=str, help=" -> username")
parser.add_argument("password", type=str, help=" -> password")
parser.add_argument("dnbase", type=str, help=" -> dnbase")

# Accept Self-Sign Certificates
# ldap.set_option(ldap.OPT_X_TLS_REQUIRE_CERT, ldap.OPT_X_TLS_NEVER)
server = Server('10.134.2.43' ,port=389, use_ssl=False, get_info=ALL_ATTRIBUTES)
#server = Server('10.4.1.47' ,port=389, use_ssl=False, get_info=ALL_ATTRIBUTES)
set_config_parameter('DEFAULT_CLIENT_ENCODING', 'utf8')
BaseAD = "ou=Utilisateurs,dc=adchpg,dc=chpg,dc=mc"
BaseeDir = "ou=Utilisateurs,ou=chm,O=chpg"
Scope = 'SUBTREE'
FilterAD = "(&(objectClass=person)(!(objectClass=computer)))"
FiltereDir = "(&(objectClass=User))"
AttrsAD = ['samAccountName','cn', 'pwdLastSet','UserAccountControl','lastlogontimestamp']
AttrseDir = ['cn','pwdChangedTime','logindisabled']
conn = Connection(server, 'cn=Netonline,ou=Externes,ou=Utilisateurs,dc=adchpg,dc=chpg,dc=mc', 'Netonline@26', auto_bind=True)
conn.search(search_base=BaseAD, search_filter=FilterAD, search_scope=Scope, attributes=AttrsAD )
#conn = Connection(server, 'cn=netonline,ou=presta,ou=ext,o=chpg', 'Netonline@26', auto_bind=True)
#conn.search(search_base=BaseeDir, search_filter=FiltereDir, search_scope=Scope, attributes=AttrseDir)

print(conn.entries)

# Retrouve la date dans la valeur dans attribut
def getFtime(pwdLastSet):
    if len(pwdLastSet or ()) == 0:
        return
    else:
        LastSet = (int(pwdLastSet) / 10000000) - 11644473600
        return(time.ctime(LastSet))

def getF2time(pwdChangedTime):
    if len(pwdChangedTime or ()) == 0:
        return
    else:
        pwdChange = str(pwdChangedTime).strip('Z')
        time_tuple = time.strptime(pwdChange, "%Y%m%d%H%M%S")
        t = calendar.timegm(time_tuple)
        return(time.ctime(t))


trustee_data = open('listAdUser.csv', 'w')
#trustee_data = open('listedirUser.csv', 'w')
csvwriter = csv.writer(trustee_data)
trustee_data_head = ['samAccountName','cn', 'pwdLastSet','UserAccountControl','lastlogontimestamp']
csvwriter.writerow(trustee_data_head)
#for row in conn.entries:
#    line = []
#    cn = (row.cn[0])
#    line.append(cn)
#    pwd = (row.pwdChangedTime)
#    line.append(getF2time(pwd))
#    logindis = (row.logindisabled)
#    line.append(logindis)
#    csvwriter.writerow(line)

for row in conn.entries:
    line = []
    sam = (row.samAccountName)
    line.append(sam)
    cn = (row.cn)
    line.append(cn)
    pwdlast = (row.pwdLastSet.value)
    line.append(getFtime(pwdlast))
    logindis = (row.UserAccountControl)
    line.append(logindis)
    lastlog = (row.lastlogontimestamp.value)
    line.append(getFtime(lastlog))
    csvwriter.writerow(line)
trustee_data.close()
