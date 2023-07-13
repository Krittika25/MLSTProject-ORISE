#!/usr/bin/env python3
'''
Script to parse the allele calls by hash-cgmlst tool 
Date: 30th June, 2023
Author: Krittika Krishnan
Usage: python parseJson.py <inputfiles> Or python parseJson.py *.json
Output file: hash-cgmlst.matrix.tsv
'''

import sys
import glob

def getAlleleCodes(jsonfile):
    #get the asm name fromt the file name
    asmname="" 
    #store the allele presence/absence info
    alleleInfo={}     
    with open(jsonfile,"r") as infile:
        for line in infile:
            line=line.rstrip().lstrip().replace('\"',"").replace(",","")
            if "name" in line:
                asmname=line.split(":")[1].replace("_output_contigs.fa","") #"name": "SRR16102703_output_contigs.fa",           
            #getting allele presence info from input file
            if "INNUENDO_" in line: #use a better pattern match for the allele names
                alleleName=line.split(":")[0]
                value=line.split(":")[1]
                #print(alleleName+"\t"+value)
                alleleInfo[alleleName]=value                        
    alleleheader=[]
    for k,v in alleleInfo.items():
        alleleheader.append(k)
        if v == ' ':
            alleleInfo[k]="-1"    
    with open("hash-cgmlst.matrix.tsv","a") as fh:    
        fh.write("Assembly"+"\t"+("\t").join(alleleheader)) #printing the header
    #fh.close()
    return asmname,alleleInfo



#Get user input
def getFiles(infiles):
    with open("hash-cgmlst.matrix.tsv","a") as fh1:    
        for file in infiles:
            #print(file) #Checking if all the file are getting processed
            asmname,alleleCodes=getAlleleCodes(file)
            alleleStatus=[]
            for k,v in alleleCodes.items():
                alleleStatus.append(v)
            fh1.write(asmname+"\t"+"\t".join(alleleStatus))
            fh1.write("\n")
        fh1.close()
        return
    


def main():
    inputfiles = sys.argv[1]
    filePaths = glob.glob("*.json") #Allowing all files to be used as input to the script.
    allFiles = []
    for filePath in filePaths:
        allFiles.append(filePath)
    getFiles(allFiles)

if __name__=="__main__":
    main()
