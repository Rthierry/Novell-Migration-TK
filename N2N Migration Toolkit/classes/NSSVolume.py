#!/usr/bin/env python3
from pymongo import MongoClient
import hashlib
import pandas as pd
import re
import pprint


class NSSVolume(object):

    client = MongoClient()
    errorLog = []
    ADLanguage = "EN"
    verbose = 0

    def __init__(self, volname, db, verbose):
        NSSVolume.volname = volname
        NSSVolume.db = db
        NSSVolume.verbose = verbose
        ### Change DB Name here
        NSSVolume.dbclient = self.client[NSSVolume.db]

        ### OES NSS material import
        NSSVolume.NSSTrusteesCollection = self.dbclient['NSSTrustees']
        NSSVolume.NSSIRFCollection = self.dbclient['NSSIrf']
        NSSVolume.NSSQuotasCollection = self.dbclient['NSSQuotas']
        NSSVolume.NSSTrusteesVersionCollection = self.dbclient['NSSTrusteesVersion']

        ### Converted permission from previous runs
        NSSVolume.NTFSAceCollection = self.dbclient['NTFSAce']
        NSSVolume.traverseFolderCollection = self.dbclient['TraverseFolderList']
        NSSVolume.traverseGroupMembershipCollection = self.dbclient['TraverseGroupMembership']
        NSSVolume.traverseRightsCollection = self.dbclient['TraverseRights']
        NSSVolume.overrideCollection = self.dbclient['OverrideTrustees']

        ##NSS version
        NSSVolume.currentVersion = self.NSSTrusteesVersionCollection.find_one({'Status' : 'Current', 'Volume' : self.volname })['Version']

        ##Import NSS Collection from DB
        NSSVolume.aceList = self.importCollectionFromDB(self.volname, self.NSSTrusteesCollection)

        ##Import Traverse Folder List from DB
        NSSVolume.traverseFolderList = self.importCollectionFromDB(self.volname, self.traverseFolderCollection)

        ##Import NTFS Ace List from DB
        NSSVolume.ntfsAceList = self.importCollectionFromDB(self.volname, self.NTFSAceCollection)

        ##Import traverse group membership table
        NSSVolume.traverseGroupMembershipList = self.importCollectionFromDB(self.volname, self.traverseGroupMembershipCollection)

        ##Import traverse right list
        NSSVolume.traverseRightsList = self.importCollectionFromDB(self.volname, self.traverseRightsCollection)

        ##NSS Quotas list
        NSSVolume.NSSQuotasList = self.importCollectionFromDB(self.volname, self.NSSQuotasCollection)

        ##NSS IRF
        NSSVolume.NSSIRFList = self.importCollectionFromDB(self.volname, self.NSSIRFCollection)

        ##Override List
        NSSVolume.overrideList = self.importCollectionFromDB(self.volname, self.overrideCollection)


    def generateRights(self):

        self.purgeCollectionByVolName(self.volname, self.NTFSAceCollection)
        self.purgeCollectionByVolName(self.volname, self.traverseGroupMembershipCollection)
        self.purgeCollectionByVolName(self.volname, self.traverseFolderCollection)
        self.convertToNTFS()
        self.generateTraverseGroup()
        self.generateTraverseRights()
        self.detectAclOverride()

        print ("Known bug : You might want to rerun NSSConverter with --detectAclOverride instead, because it does not work on the first run.")



    # -----------------------------------------------
    # -----------   Traverse Group ------------------
    # -----------------------------------------------
    def generateTraverseGroup(self):
        if (self.verbose): print ("Generating Traverse path")
        count = 0
        for row in NSSVolume.ntfsAceList:
            currentPath = row['Path']
            while(currentPath.count("/") >= 1 ):                
                previousPath = currentPath
                currentPath = self.getParentFolder(currentPath)
                groupName = self.generateTraverseGroupName(currentPath)
                post = { "Volume" : self.volname, "Path" : currentPath, 'Group' : groupName, 'Version' : self.currentVersion }
                count = count + 1
                self.insertLineToDB(post, self.traverseFolderCollection, 1)
                self.traverseFolderCollection.update({"Path": previousPath, "Volume" : self.volname, "Version" : self.currentVersion }, {"$set": {"ParentFolder": currentPath, "MemberOf" : groupName, "Version" : self.currentVersion}})

        print ("Added "+str(count)+" entry to traverse folder list")


    #### Description  Add Trustee to traverse Group
    @classmethod
    def generateTraverseRights(self):
        count = 0
        if (self.verbose): print("Generating traverse rights")
        ### For each row in NTFS ACE List
        for row in self.ntfsAceList:

            ### Query the Traverse Folder DB with the path of the permission parent Folder
            parentFolder = self.traverseFolderCollection.find( { 'Path' : self.getParentFolder(row['Path']), 'Version' : self.currentVersion, 'Volume' : self.volname })
            ### For the uniq result
            for f in parentFolder:
                count = count + 1
                self.insertLineToDB({ 'Volume' : self.volname ,'SAMAccountName' : row['SAMAccountName'], 'MemberOf' : f['Group'], 'Version' : self.currentVersion}, self.traverseGroupMembershipCollection, 1)
                ### Add the trustee to the group
                if (self.verbose): print ("Adding "+row['SAMAccountName']+" to : "+f['Group'])

        for value in self.traverseFolderList:
            #print (value.keys())
            if "MemberOf" in value.keys():
                if (self.verbose): print ("Group "+value['Group']+" member of "+value['MemberOf'])
                count = count + 1
                self.insertLineToDB({ 'Volume' : self.volname, 'SAMAccountName' : value['Group'], 'MemberOf' : value['MemberOf'], 'Version' : self.currentVersion}, self.traverseGroupMembershipCollection, 1)
                post = {'Volume' : self.volname, 'Type' : "TraverseRights", 'SAMAccountName' : value['Group'], 'Path' : value['Path'], 'Rights' : "Read,ReadAndExecute,Synchronize", 'Scope' : "ThisFolderOnly", 'Version' : self.currentVersion }                
                self.insertLineToDB(post, self.NTFSAceCollection, 1)
        

        print ("Added "+str(count)+" entry to GroupMembership collection")

    # -----------------------------------------------
    # -----------   Extraction Method ---------------
    # -----------------------------------------------
    @classmethod
    def importCollectionFromDB(self, volname, collection):

        acelist = collection.find({ 'Volume' : volname, 'Version' : self.currentVersion})
        return acelist

    @classmethod
    def requestTrusteesDict(self, query):
        result = self.NSSTrusteesCollection.find(query, { '_id' : False, 'Version' : False})
        return result

    # -----------------------------------------------
    # -------   Database Modification Method --------
    # -----------------------------------------------

    @classmethod
    def purgeCollectionByVolName(self, volname, collection):
        if (self.verbose): print ("Delete collection for",volname)
        result = collection.delete_many({ "Volume" : volname})

    @classmethod
    def insertLineToDB(self, post, collection, uniq=None):
        uniqueFilter = {}
        if ( uniq is not None):
            for index, row in post.items():
                uniqueFilter[index] = row
                #print (uniqueFilter)
            post_id = collection.update_one(post, { '$set' : post }, upsert=True)
        else:
            #post = { "Volume" : self.volname, "Path" : post['Path'], "Rights" : post['Rights'], "SAMAccountName" : post['SAMAccountName']}
            post_id = collection.insert_one(post).inserted_id

    ##Insert an array of dictionary to MongoDB
    @classmethod
    def insertToDB(self, rowlist, collection, volname, filter=None):
        count = 0

        for row in rowlist:
            count = count + 1
            #post = { "Volume" : volname, "Path" : row['Path'], "Rights" : row['Rights'], "SAMAccountName" : row['SAMAccountName']}

            if (filter is None):
                self.insertLineToDB(row, collection)
            else:
                self.insertLineToDB(row,collection,1)

        print ("Inserted "+str(count)+" rows into database for "+volname)

    # -----------------------------------------------
    # -------   Database Modification Method --------
    # -----------------------------------------------
    @classmethod
    def convertToNTFS(self):
        convertedRights = []
        countNormal = 0
        countOU = 0
        for trustee in self.aceList:
            username = self.extractUserName(trustee['name'])
            path = trustee['path']
            right = self.aceToNTFS(trustee['rights'])

            if (re.match("\.OU=.*T=.*",trustee['name'])):
                countOU = countOU + 1
                convertedRights.append( { 'Volume' : self.volname, 'Type' : 'OUConvertedRight' ,'SAMAccountName' : username, 'Path' : path, 'Rights' : right, 'Scope' : 'ThisFolderSubFoldersAndFiles', 'Version' : self.currentVersion })
            else:
                countNormal = countNormal + 1
                convertedRights.append( { 'Volume' : self.volname, 'Type' : 'UsualConvertedRight' ,'SAMAccountName' : username, 'Path' : path, 'Rights' : right, 'Scope' : 'ThisFolderSubFoldersAndFiles', 'Version' : self.currentVersion })

        self.ntfsAceList = convertedRights
        self.purgeCollectionByVolName(self.volname, self.NTFSAceCollection)
        self.insertToDB(self.ntfsAceList, self.NTFSAceCollection, self.volname, "toto")
        print ("Type : "+str(countNormal)+" standard ACE ")
        print ("Type : "+str(countOU)+" OU ACE ")

    ### Take NSS ACE string in and return NTFS ACE string
    @classmethod
    def aceToNTFS(self, right):

        ace = []
        if "r" in right: ace.append("Read,ReadAndExecute,Synchronize")
        if "w" in right: ace.append("Write")
        if "e" in right: ace.append("Delete")
        if "c" in right: ace.append("CreateFiles,CreateDirectories")
        if "m" in right: ace.append("Modify")
        if "f" in right: ace.append("ListDirectory")
        if "a" in right: ace.append("ReadPermissions,ChangePermissions")
        if "s" in right: ace.append("FullAccess")
        return (",".join([ entry for entry in ace ]))

    ### Take NSS Rights as string and return dictionary
    @classmethod
    def aceToNTFSDict(self, right):
        rights = ""

        if "r" in right: Read, ReadAndExecute, Synchronize = 1
        if "w" in right: Write = 1
        if "e" in right: Delete = 1
        if "c" in right: CreateFiles, CreateDirectories = 1
        if "m" in right: Modify = 1
        if "f" in right: ListDirectory = 1
        if "a" in right: ReadPermissions, ChangePermissions = 1
        if "s" in right: FullAccess = 1
        return ({   'Read' : Read,
                    'ReadAndExecute' : ReadAndExecute,
                    'Synchronize' : Synchronize,
                    "Write" : Write,
                    "Delete" : Delete,
                    "CreateFiles" : CreateFiles,
                    "CreateDirectories" : CreateDirectories,
                    "Modify" : Modify,
                    "ListDirectory" : ListDirectory,
                    "ReadPermissions" : ReadPermissions,
                    "ChangePermissions" : ChangePermissions,
                    "FullAccess" : FullAccess
                })


    # -------------------------------------------------
    # -------------   Conversion Method  --------------
    # -------------------------------------------------

    @classmethod
    def dict_compare(self, d1, d2):
        d1_keys = set(d1.keys())
        d2_keys = set(d2.keys())
        intersect_keys = d1_keys.intersection(d2_keys)
        added = d1_keys - d2_keys
        removed = d2_keys - d1_keys
        modified = {o : (d1[o], d2[o]) for o in intersect_keys if d1[o] != d2[o]}
        same = set(o for o in intersect_keys if d1[o] == d2[o])
        return added, removed, modified, same


    @classmethod
    def showDifferences(self,preversion, postversion):        
        preTrustees = self.requestTrusteesDict({'Volume' : self.volname, 'Version' : int(preversion)})
        postTrustees = self.requestTrusteesDict({'Volume' : self.volname, 'Version' : int(postversion)})
        changelist = []

        for element in preTrustees:
            query = { 'Volume' : self.volname, 'Version' : int(postversion), 'TID' : element['TID'], 'path' : element['path']}
            result = self.NSSTrusteesCollection.find_one(query) 

            if (result == None):
                change = { 'Status' : 'Removed', 'Path' : element['path'], 'Rights' : element['rights'], 'Name' : element['name'] }
                changelist.append(change)
            else:
                if ( result['rights'] not in element['rights']):
                    change = { 'Status' : 'Modified', 'Path' : result['path'], 'Rights' : result['rights'], 'OldRights' : element['rights'], 'Name' : result['name'] }
                    changelist.append(change)
            
        for element in postTrustees:
            query = { 'Volume' : self.volname, 'Version' : int(preversion), 'TID' : element['TID'], 'path' : element['path']}
            result = self.NSSTrusteesCollection.find_one(query) 
            if (result == None):  
                change = { 'Status' : 'Added', 'Path' : element['path'], 'Rights' : element['rights'], 'Name' : element['name'] }              
                changelist.append(change)
        
        pd.DataFrame(list(changelist)).to_csv(self.volname+"-diff.csv")

        if ( self.verbose ):
            for element in changelist:
                print (element)

        



    @classmethod
    def extractUserName(self, fqdn):

        ### Usual CN
        if (re.match("\.CN.*\.T=.*", fqdn)):
            username = fqdn.split(".")[1].split("=")[1]
            return username


        ### If username is "\\", then it might come from AD integration
        elif (re.match(".*\\\\.*",fqdn)):
            username = fqdn.split("\\")[1]
            return username

        ### If between [], then check for special trustee
        elif (re.match("\[.*\]",fqdn)):
            if ( ("[Public]" in fqdn) or ("[Root]" in fqdn)):
                if ("FR" in self.ADLanguage):
                    return "Utilisa. du domaine"
                elif("EN" in self.ADLanguage):
                    return "Domain Users"

        ## If trustee is OU        
        elif(re.match("\.OU=.*T=.*",fqdn)):            
            ## Then generate group using whole fqdn -> grp--ou-ou-ou-o 
            username = ""

            ## Skip first cell in array because null, and stop before treename -> [1:-2]
            for part in fqdn.split(".")[1:-2]:

                ## if string isn't empty then add to group name
                if ( part != "" ):
                    #print ( str(part.split("=")) )
                    username = username + "-" +part.split("=")[1]

            
            return ("grp-"+username)
        else:
            return "Unknown user"

    @classmethod
    def getParentFolder(self,path):
        parentFolder = path.rsplit("/",1)[0]
        return parentFolder


    @classmethod
    def getParentFolderList(self, path):

        folderList = []
        currentPath = path

        while(currentPath.count("/") > 1 ):
            currentPath = self.getParentFolder(currentPath)
            folderList.append(currentPath)

        return folderList

    @classmethod
    def generateTraverseGroupName(self, path):

        ##Remove slash character from path
        noslashpath = path.replace("/","")
        noslashpath = path.replace(" ","")
        noslashpath = self.volname + noslashpath
        hashpath = hashlib.md5(noslashpath.encode('utf-8')).hexdigest()

        trunkpath = ""
        for folder in path.split("/")[1:]:
            trunkpath = trunkpath + folder[0:3].replace(" ","")            

        return (self.volname+"-"+trunkpath+"-"+hashpath[0:10])[0:60]

    @classmethod
    def detectAclOverride(self):
        print ("ACL Override detection ran")
        for trustee in self.aceList:
            parentFolders = self.getParentFolderList(trustee['path'])            
            override = 0
            for folder in parentFolders:
                parentTrustee = self.NSSTrusteesCollection.find_one({ 'path' : folder, 'name' : trustee['name'] })

                if (parentTrustee != None):
                    post = { 'Type' : 'InitialFolder', 'Path' : trustee['path'], 'Name' : trustee['name'], 'Right' : trustee['rights'], 'Volume' : self.volname, 'Version' : self.currentVersion }
                    self.insertLineToDB(post, self.overrideCollection)
                    if ( self.verbose): print ("Initial Folder :"+trustee['path'],"for",trustee['name'],"and right",trustee['rights'])
                    post = { 'Type' : 'Override', 'Path' : parentTrustee['path'], 'Name' : parentTrustee['name'], 'Right' : parentTrustee['rights'], 'Volume' : self.volname, 'Version' : self.currentVersion }
                    self.insertLineToDB(post, self.overrideCollection)
                    if ( self.verbose): print ("Override : ",parentTrustee['path'],"for",parentTrustee['name'],"with acl",parentTrustee['rights'])
                    override = 1

            if (override == 1):
                for folder in parentFolders:
                    irf = self.NSSIRFCollection.find_one({'Path' : folder})
                    if (irf != None):
                        post = { 'Type' : 'IRF', 'Path' : folder, 'Right' : irf['Filter'], 'Volume' : self.volname, 'Version' : self.currentVersion  }
                        self.insertLineToDB(post, self.overrideCollection)
                        if ( self.verbose): print("Found IRF on "+folder+" with filter :",irf['Filter'])
                override = 0

        print ("Result exported to OverrideTrustees collection.")




    # -------------------------------------------------
    # -------------   Export Method  ------------------
    # -------------------------------------------------



    @classmethod
    def exportToCSV(self):

        pd.DataFrame(list(self.ntfsAceList)).to_csv(self.volname+"-ntfs.csv")
        pd.DataFrame(list(self.aceList)).to_csv(self.volname+"-nss.csv")
        pd.DataFrame(list(self.traverseFolderList)).to_csv(self.volname+"-travFolder.csv")
        pd.DataFrame(list(self.traverseGroupMembershipList)).to_csv(self.volname+"-travGrpMembership.csv")
        pd.DataFrame(list(self.NSSQuotasList)).to_csv(self.volname+"-quotas.csv")
        pd.DataFrame(list(self.NSSIRFList)).to_csv(self.volname+"-irf.csv")
        pd.DataFrame(list(self.overrideList)).to_csv(self.volname+"-override.csv")

        print ("NSS Permission : "+self.volname+"-nss.csv")
        print ("NTFS Permission : "+self.volname+"-ntfs.csv")
        print ("Traverse Group Membership : "+self.volname+"-travGrpMembership.csv")
        print("NSS Quotas : "+self.volname+"-quotas.csv")
        print("NSS IRF : "+self.volname+"-irf.csv")
        print("Override List : "+self.volname+"-override.csv")
