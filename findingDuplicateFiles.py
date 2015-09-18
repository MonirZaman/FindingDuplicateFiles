# -*- coding: utf-8 -*-
"""
@author: Monir Zaman
University of Calgary
mzn.munnaATgmailDOTcom

Problem description: A Linux directory structure contains 100G worth of files. The
                     depth and number of sub-directories and files is not known.
                     Soft-links and hard-links can also be expected.  Write, in
                     the language of your choice, a program that traverses the
                     whole structure as fast as possible and reports duplicate
                     files. Duplicates are files with same content.

Solution overview: Files are first clustered based on their sizes. Two files with the same size
                   will be in the same cluster. Clusters that contains only one file are filtered out.
                   Files are re clustered using the md5 hash of their content. This time, two files
                   will be in the same cluster only if their content is same.
                   
                   Since the number of files is huge (their size can be huge too), we first cluster 
                   based file size and reduce the number of candidate clusters by filtering out
                   single element list.

Command to run the code: python findingDuplicateFiles.py <directoryName>
"""

import hashlib, os,sys

def fileSize(pathAndFilename):
    """
    Returns the size of the file denoted by pathAndFilename
    """
    return os.stat(pathAndFilename).st_size

def md5Hash(pathAndFilename, blockSize=8192):
    """
    Generate md5 hash of the file pathAndFilename.
    The entire file is not loaded into the memory as it may exceed the memory. Rather,
    its hash is computed by reading one block of its at a time.
        
    Args: 
        pathAndFilename: input file name 
        blockSize: refers the size of the block read from the file each time. It is a multiple of 128
    """
    hashcode = hashlib.md5()
    with open(pathAndFilename, "rb" ) as f:
        block = f.read(blockSize)
        while len(block)>0:
            hashcode.update(block)
            block = f.read(blockSize)
    return hashcode.hexdigest()


class Cluster():
    """
    Class containing data structure and code for clustering files based on a 
    given key (either size or content)
    """
    def __init__(self):
        """
        keyingMethod is a reference of the method to produce a key for an 
        input file based on the file's size or content.
        keyToFile is a dictionary where is key is a file property 
        and value is the list of files that have the property
        """
        self.keyingMethod=fileSize
        self.keyToFile=dict()
        
    
    def getKey(self,pathAndFilename):
        """
        Wrapper method that calls keyingMethod and returns the key representing 
        input file pathAndFilename
        """
        return self.keyingMethod(pathAndFilename)
  
    
    def addFile(self,pathAndFilename):
        """
        Adds a file's key and path to the dictionary keyToFile if the file is seen for the first time
        Files that have been seen before are added to the list of paths which is the value for the key  
        """
        #generate the key for the file
        fkey=self.getKey(pathAndFilename)
        
        #Checking if the key was seen before; if so, then file has duplicates
        if self.keyToFile.has_key(fkey):
            self.keyToFile[fkey].append(pathAndFilename)
        else:
            self.keyToFile[fkey]=[pathAndFilename]
    
    def reset(self):
        """
        Reset the data structure keyToFile to an empty dictionary
        """
        self.keyToFile=dict()
        
    def getClusters(self):    
        """
        Performs the following:
        1. Filters out single element list in the self.keyToFile
        2. reset self.keyToFile
        3. Returns remaining lists
        """
        clusters=filter(lambda lst:len(lst)>1,self.keyToFile.values())
        self.reset()
        return clusters
    
    def clustering(self):
        """
        Performs the remaining clustering operations. Note that the initial scan of 
        of the directory using os.walk (in scanDirectory method) grouped a file 
        by calling addFile method. clustering method starts where the initial scan left off
        
        Output: print cluster of duplicate files to the console
        """        
        clusterOfFiles=self.getClusters()
        
        #group files based on the hash of their contents
        self.keyingMethod=md5Hash
        [self.addFile(afile) for acluster in clusterOfFiles for afile in acluster]
        clusterOfFiles=self.getClusters()
        self.showClusters(clusterOfFiles)
        
    
    def showClusters(self,clusterOfFiles,batchSize=3):
        """
        Print clusters of duplicate files
        Args:
            clusterOfFiles: a list of 1D list. All files within an 1D list are duplicates
            batchSize: the number of clusters to print at a time
        """
        #groupCounter keeps track of how many clusters of duplicate files has been printed
        clusterCounter=0
        for acluster in clusterOfFiles:
            #print a cluster/group of duplicate files
            print("Duplicate group {0}".format(clusterCounter+1))
            print ("All of these files have the same content:")
            for afile in acluster:
                print(afile)
            
            #increase the groupCounter by 1 as one group has been printed
            clusterCounter+=1
            if clusterCounter%batchSize==0:
                raw_input("Press any key for more duplicates")
#end of the class
          
def scanDirectory(directoryName="."):
    """
    List the files in the directoryName and its sub directories,
    pass them to cluster object and calls the clustering method of the object
    """
    cluster=Cluster()

    #reading files and folders    
    for path, folders, files in os.walk(directoryName):
        for afile in files:
            cluster.addFile(os.path.join(path,afile))
    
    cluster.clustering()

if __name__=="__main__":
    if len(sys.argv)>1:
        scanDirectory(sys.argv[1])
    #scanDirectory()