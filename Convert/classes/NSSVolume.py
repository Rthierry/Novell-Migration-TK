#!/usr/bin/env python3
from pymongo import MongoClient
import hashlib

class NSSVolume(object):

    client = MongoClient()

    def __init__(self, volname, db):
        NSSVolume.volname = volname
        NSSVolume.db = db

        ### Change DB Name here
        NSSVolume.dbclient = self.client[NSSVolume.db]
        NSSVolume.NTFSAceCollection = self.dbclient['NTFSAce']
        NSSVolume.NSSTrusteesCollection = self.dbclient['NSSTrustees']
        NSSVolume.traverseFolderCollection = self.dbclient['TraverseFolderList']
        NSSVolume.traverseGroupMembershipCollection = self.dbclient['TraverseGroupMembership']
        NSSVolume.traverseRightsCollection = self.dbclient['TraverseRights']

        ##Import NSS Collection from DB
        NSSVolume.aceList = self.importCollectionFromDB(self.volname, self.NSSTrusteesCollection)

        ##Import Traverse Folder List from DB
        NSSVolume.traverseFolderList = self.importCollectionFromDB(self.volname, self.traverseFolderCollection)

        ##Import NTFS Ace List from DB
        NSSVolume.ntfsAceList = self.importCollectionFromDB(self.volname, self.NTFSAceCollection)

        ##Import traverse group membership table
        NSSVolume.traverseGroupMembershipList = self.importCollectionFromDB(self.volname, self.traverseGroupMembershipCollection)

        NSSVolume.traverseRightsList = self.importCollectionFromDB(self.volname, self.traverseRightsCollection)

    def generateRights(self):
        self.convertToNTFS()
        self.generateTraverseGroup()
        self.generateTraverseRights()




    def generateTraverseGroup(self):
        print ("Generating Traverse path")

        for row in NSSVolume.ntfsAceList:
            currentPath = self.getParentFolder(row['Path'])
            while(currentPath.count("/") > 1 ):
                previousPath = currentPath
                currentPath = self.getParentFolder(currentPath)
                noslashpath = currentPath.replace("/","")
                noslashpath = currentPath.replace(" ","")
                hashpath = hashlib.md5(noslashpath.encode('utf-8')).hexdigest()

                trunkpath = ""
                for folder in currentPath.split("/")[1:]:
                    trunkpath = trunkpath + folder[0:3]

                groupName = ("TRVGRP-"+trunkpath+"-"+hashpath[0:10])[0:60]
                post = { "Volume" : self.volname, "Path" : currentPath, 'Group' : groupName }
                self.insertLineToDB(post, self.traverseFolderCollection, 1)
                self.traverseFolderCollection.update({"Path": previousPath}, {"$set": {"ParentFolder": currentPath, "MemberOf" : groupName}})
                #print (post)


    def getParentFolderList(self, path):

        folderList = []
        currentPath = path

        while(currentPath.count("/") > 1 ):
            currentPath = self.getParentFolder(currentPath)
            folderList.append(currentPath)

        return folderList


    #### Description  Add Trustee to traverse Group
    @classmethod
    def generateTraverseRights(self):
        print("Generating traverse rights")
        ### For each row in NTFS ACE List
        for row in self.ntfsAceList:

            ### Query the Traverse Folder DB with the path of the permission parent Folder
            parentFolder = self.traverseFolderCollection.find( { 'Path' : self.getParentFolder(row['Path']) })
            ### For the uniq result
            for f in parentFolder:
                self.insertLineToDB({ 'Volume' : self.volname ,'SAMAccountName' : row['SAMAccountName'], 'MemberOf' : f['Group']}, self.traverseGroupMembershipCollection, 1)
                ### Add the trustee to the group
                print ("Adding "+row['SAMAccountName']+" to : "+f['Group'])

        for value in self.traverseFolderList:
            if "MemberOf" in value.keys():
               print ("Group "+value['Group']+" member of "+value['MemberOf'])
               self.insertLineToDB({ 'Volume' : self.volname, 'SAMAccountName' : value['Group'], 'MemberOf' : value['MemberOf']}, self.traverseGroupMembershipCollection, 1)
               self.insertLineToDB({'Volume' : self.volname, 'Type' : "TraverseRights", 'SAMAccountName' : value['Group'], 'Path' : value['Path'], 'Rights' : "Read,ReadAndExecute,Synchronize", 'Scope' : "ThisFolderOnly" }, self.NTFSAceCollection, 1)








    @classmethod
    def generateTraversePaths(self):
        for row in NSSVolume.ntfsAceList:
            #print ("Initial : " + row['Path'])
            currentPath = self.getParentFolder(row['Path'])
            while(currentPath.count("/") > 1 ):
                currentPath = self.getParentFolder(currentPath)
                #print("Parent Folder : " + currentPath)
                post = { "Volume" : self.volname, "Path" : currentPath, "MemberOf" : "", "ParentFolder" : "" }
                self.insertLineToDB(post, self.traverseFolderCollection, 1)


    @classmethod
    def generateTraverseGroupName(self, path):
        ##Remove slash character from path
        noslashpath = path.replace("/","")
        noslashpath = path.replace(" ","")
        hashpath = hashlib.md5(noslashpath.encode('utf-8')).hexdigest()

        trunkpath = ""
        for folder in path.split("/")[1:]:
            trunkpath = trunkpath + folder[0:3]

        return (trunkpath+"-"+hashpath[0:10])[0:60]



    @classmethod
    def getParentFolder(self,path):
        parentFolder = path.rsplit("/",1)[0]
        return parentFolder
        #noslash = parentFolder.replace("/", "")
        #print ("Noslash : "+noslash)

    @classmethod
    def purgeCollectionByVolName(self, volname, collection):
        print ("Delete collection for",volname)
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

        print ("Inserted "+str(count)+" rows into for "+volname)

    @classmethod
    def convertToNTFS(self):
        convertedRights = []
        for trustee in self.aceList:
            username = self.extractUserName(trustee['Trustee'])
            path = trustee['Path']
            right = self.aceToNTFS(trustee['Rights'])
            convertedRights.append( { 'Volume' : self.volname, 'Type' : 'ConvertedRight' ,'SAMAccountName' : username, 'Path' : path, 'Rights' : right, 'Scope' : 'ThisFolderSubFoldersAndFiles' })

        self.ntfsAceList = convertedRights
        self.purgeCollectionByVolName(self.volname, self.NTFSAceCollection)
        self.insertToDB(self.ntfsAceList, self.NTFSAceCollection, self.volname, "toto")

    @classmethod
    def importCollectionFromDB(self, volname, collection):
        acelist = collection.find({ 'Volume' : volname})
        return acelist


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

    @classmethod
    def extractUserName(self, fqdn):
        username = fqdn.split(".")[1].split("=")[1]
        return username
