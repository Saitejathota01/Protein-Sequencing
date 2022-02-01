"""
Protein Sequencing Project
Name:
Roll Number:
"""

from asyncore import read
from turtle import width
import hw6_protein_tests as test

project = "Protein" # don't edit this

### WEEK 1 ###

'''
readFile(filename)
#1 [Check6-1]
Parameters: str
Returns: str
'''
def readFile(filename):
    file= open(filename,"r")
    read=file.read()
    str=""
    for line in read.splitlines():
        str= str+line
    return str
    


'''
dnaToRna(dna, startIndex)
#2 [Check6-1]
Parameters: str ; int
Returns: list of strs
'''
def dnaToRna(dna, startIndex):
    condonlist = []
    stop_codons = ["UGA","UAG","UAA"]
    for word in range(startIndex,len(dna),3):
        dna = dna.replace("T","U")
        condon = dna[word:word+3]
        if condon not in stop_codons:
            condonlist.append(condon)
        else:
            condonlist.append(condon)
            break
    return condonlist



'''
makeCodonDictionary(filename)
#3 [Check6-1]
Parameters: str
Returns: dict mapping strs to strs
'''
def makeCodonDictionary(filename):
    import json
    file = open(filename,"r")
    proteins = json.load(file)
    codon_dict= {}
    for key in proteins:
        for values in proteins[key]:
            values = values.replace("T","U")
            codon_dict[values] = key
    return codon_dict




'''
generateProtein(codons, codonD)
#4 [Check6-1]
Parameters: list of strs ; dict mapping strs to strs
Returns: list of strs
'''
def generateProtein(codons, codonD):
    proteinlist = []
    for rna in codons:
        for rnaproteins in codonD:
            if rna == rnaproteins:
                proteinlist.append(codonD[rnaproteins])
                if proteinlist[0] == "Met":
                    proteinlist[0] = "Start"
    return proteinlist
    


'''
synthesizeProteins(dnaFilename, codonFilename)
#5 [Check6-1]
Parameters: str ; str
Returns: 2D list of strs
'''
def synthesizeProteins(dnaFilename, codonFilename):
    rna_list = readFile(dnaFilename)
    protein_list = makeCodonDictionary(codonFilename)
    totalprotein_list = []
    codons = 0
    unusedltrs = 0
    while codons<len(rna_list) :
        word = rna_list[codons:codons+3]
        if word == "ATG":
            rna = dnaToRna(rna_list, codons)
            totalprotein_list.append(generateProtein(rna,protein_list))
            codons = codons+3*len(rna)
        else:
            unusedltrs += 1
            codons += 1      
    return totalprotein_list
    


def runWeek1():
    print("Human DNA")
    humanProteins = synthesizeProteins("data/human_p53.txt", "data/codon_table.json")
    print("Elephant DNA")
    elephantProteins = synthesizeProteins("data/elephant_p53.txt", "data/codon_table.json")


### WEEK 2 ###

'''
commonProteins(proteinList1, proteinList2)
#1 [Check6-2]
Parameters: 2D list of strs ; 2D list of strs
Returns: 2D list of strs
'''
def commonProteins(proteinList1, proteinList2):
    commonprtein_list = []
    for protein_1 in proteinList1:
        for protein_2 in proteinList2:
            if protein_1 == protein_2 and protein_1 not in commonprtein_list:
                commonprtein_list.append(protein_1)
    return commonprtein_list
    


'''
combineProteins(proteinList)
#2 [Check6-2]
Parameters: 2D list of strs
Returns: list of strs
'''
def combineProteins(proteinList):
    protein_list = []
    for list in proteinList:
        for proteins in list:
            protein_list.append(proteins)
    return protein_list


'''
aminoAcidDictionary(aaList)
#3 [Check6-2]
Parameters: list of strs
Returns: dict mapping strs to ints
'''
def aminoAcidDictionary(aaList):
    aminoacid_dict = {}
    for word in aaList:
        if word not in aminoacid_dict:
            aminoacid_dict[word] = 0
        if word in aminoacid_dict:
            aminoacid_dict[word] += 1
    return aminoacid_dict
    


'''
findAminoAcidDifferences(proteinList1, proteinList2, cutoff)
#4 [Check6-2]
Parameters: 2D list of strs ; 2D list of strs ; float
Returns: 2D list of values
'''
def findAminoAcidDifferences(proteinList1, proteinList2, cutoff):
    result=[]
    proteins1=combineProteins(proteinList1)
    proteins2=combineProteins(proteinList2)
    aminoDict1=aminoAcidDictionary(proteins1)
    aminoDict2=aminoAcidDictionary(proteins2)
    count1=len(proteins1)
    count2=len(proteins2)
    for amino in aminoDict1:
        if amino not in aminoDict2:
            aminoDict2[amino]=0.0
        aminoDict1[amino]/=count1           
    for amino in aminoDict2:
        if amino not in aminoDict1:
            aminoDict1[amino]=0.0
        aminoDict2[amino]/=count2  
    for aminoAcid in aminoDict1:
        if aminoAcid not in["Start","Stop"]:
                freq1= aminoDict1[aminoAcid]
                freq2= aminoDict2[aminoAcid]
                if abs(freq1-freq2)> cutoff:
                    temp=[]
                    temp.append(aminoAcid)
                    temp.append(freq1)
                    temp.append(freq2)
                    result.append(temp)
    return result
    


'''
displayTextResults(commonalities, differences)
#5 [Check6-2]
Parameters: 2D list of strs ; 2D list of values
Returns: None
'''
def displayTextResults(commonalities, differences):
    common_proteins = []
    diffamino_acids = []
    str = ''
    print("The following proteins occurred in both DNA Sequences:")
    for common in commonalities:
        if common not in common_proteins:
            common_proteins.append(common[1:-1])
    for aminoacids in common_proteins:
        if len(aminoacids) > 0:
            aminoacids = '-'.join(aminoacids)
            diffamino_acids.append(aminoacids)
    diffamino_acids.sort()
    for l in diffamino_acids:
        str += ' '+ l +"\n"
    print(str)
    print("The following amino acids occurred at very different rates in the two DNA sequences:")
    for b in differences:
        wrd = b[0]
        seq1 = round(b[1]*100,2)
        seq2 = round(b[2]*100,2)
        print(f"{wrd}:{seq1}% in Seq1, {seq2}% in seq2")
    return 




def runWeek2():
    humanProteins = synthesizeProteins("data/human_p53.txt", "data/codon_table.json")
    elephantProteins = synthesizeProteins("data/elephant_p53.txt", "data/codon_table.json")

    commonalities = commonProteins(humanProteins, elephantProteins)
    differences = findAminoAcidDifferences(humanProteins, elephantProteins, 0.005)
    displayTextResults(commonalities, differences)


### WEEK 3 ###

'''
makeAminoAcidLabels(proteinList1, proteinList2)
#2 [Hw6]
Parameters: 2D list of strs ; 2D list of strs
Returns: list of strs
'''
def makeAminoAcidLabels(proteinList1, proteinList2):
    aminoacid_1=combineProteins(proteinList1)
    aminoacid_2=combineProteins(proteinList2)
    uniqueAminoAcids=[]
    for amino in aminoacid_1+aminoacid_2:
        if amino not in uniqueAminoAcids:
            uniqueAminoAcids.append(amino)
    uniqueAminoAcids.sort()
    return uniqueAminoAcids
    


'''
setupChartData(labels, proteinList)
#3 [Hw6]
Parameters: list of strs ; 2D list of strs
Returns: list of floats
'''
def setupChartData(labels, proteinList):
    aminoAcids=combineProteins(proteinList)
    aminoAcidDict=aminoAcidDictionary(aminoAcids)
    aminoAcidFreq=[]
    for amino in labels:
        if amino in  aminoAcidDict:
            aminoAcidFreq.append(aminoAcidDict[amino]/len(aminoAcids))
        else:
            aminoAcidFreq.append(0)
    return aminoAcidFreq
    


'''
createChart(xLabels, freqList1, label1, freqList2, label2, edgeList=None)
#4 [Hw6] & #5 [Hw6]
Parameters: list of strs ; list of floats ; str ; list of floats ; str ; [optional] list of strs
Returns: None
'''
def createChart(xLabels, freqList1, label1, freqList2, label2, edgeList=None):
    import matplotlib.pyplot as plt
    wdth = 0.35  # the width of the bars
    plt.bar(xLabels, freqList1, width=-wdth, align='edge', label=label1,edgecolor=edgeList)
    plt.bar(xLabels, freqList2, width=wdth, align='edge', label=label2,edgecolor=edgeList) 
    title="Side by Side Bar Plot"
    plt.xticks(rotation="vertical")
    plt.legend()
    plt.title(title)
    plt.show()
    return None
    


'''
makeEdgeList(labels, biggestDiffs)
#5 [Hw6]
Parameters: list of strs ; 2D list of values
Returns: list of strs
'''
def makeEdgeList(labels, biggestDiffs):
    Colors=[]
    BigDiffList=[]
    for amino in range(len(biggestDiffs)):
        BigDiffList.append(biggestDiffs[amino][0])
    for label in labels:
        if label in BigDiffList:
            Colors.append("black")
        else: Colors.append("white")
    return Colors



'''
runFullProgram()
#6 [Hw6]
Parameters: no parameters
Returns: None
'''
def runFullProgram():
    return


### RUN CODE ###

# This code runs the test cases to check your work
if __name__ == "__main__":
    # print("\n" + "#"*15 + " WEEK 1 TESTS " +  "#" * 16 + "\n")
    # test.week1Tests()
    # print("\n" + "#"*15 + " WEEK 1 OUTPUT " + "#" * 15 + "\n")
    # runWeek1()
    #test.testReadFile()
    #test.testDnaToRna()
    #test.testMakeCodonDictionary()
    #test.testGenerateProtein()
    #test.testGenerateProtein()
    #test.testSynthesizeProteins()

    ## Uncomment these for Week 2 ##

    # print("\n" + "#"*15 + " WEEK 2 TESTS " +  "#" * 16 + "\n")
    # test.week2Tests()
    # print("\n" + "#"*15 + " WEEK 2 OUTPUT " + "#" * 15 + "\n")
    # runWeek2()
    #test.testCommonProteins()
    #test.testCombineProteins()
    #test.testAminoAcidDictionary()
    #test.testFindAminoAcidDifferences()
    


    
    

    ## Uncomment these for Week 3 ##
    
    print("\n" + "#"*15 + " WEEK 3 TESTS " +  "#" * 16 + "\n")
    test.week3Tests()
    print("\n" + "#"*15 + " WEEK 3 OUTPUT " + "#" * 15 + "\n")
    runFullProgram()
    #test.testMakeAminoAcidLabels()
    #test.testSetupChartData()
    #test.testSetupChartData()
    test.testMakeEdgeList()
