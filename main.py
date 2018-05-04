# -*- coding: utf-8 -*-
import json
from pprint import pprint
from pymongo import MongoClient
import logging 

dotCode = ['dotCodeRecord_2016_10_1.json', 'dotCodeRecord_2016_11_1.json', 'dotCodeRecord_2016_11_2.json', 'dotCodeRecord_2016_11_3.json', 'dotCodeRecord_2016_12_1.json',\
            'dotCodeRecord_2016_12_2.json', 'dotCodeRecord_2017_10_1.json', 'dotCodeRecord_2017_10_2.json', 'dotCodeRecord_2017_10_3.json', 'dotCodeRecord_2017_10_4.json',\
            'dotCodeRecord_2017_10_5.json', 'dotCodeRecord_2017_10_6.json', 'dotCodeRecord_2017_10_7.json', 'dotCodeRecord_2017_10_8.json', 'dotCodeRecord_2017_11_1.json']

english = ['englishStarDefault_1.json', 'englishStarDefault_2.json', 'englishStarDefault_3.json', 'wellKnowCount_1.json']
vocabulary = []
for i in range(27):
    vocabulary.append('vocabularyCount_' + str(i+1) + '.json')

client = MongoClient('localhost', 27017)
db = client['steelGrade']
collection = db['vocCount']

def countAllVocabulary():
    dic = []
    for i in range(vocabulary):
        directory = 'english/' + vocabulary[i]
        doc = open(directory, 'r')
        for line in doc.readlines():
            data = json.loads(line)
            if not(data['_id']['vocabulary'] in dic):
                dic.append(data['_id']['vocabulary'])

    print("finish")

    f = open('vocAll.txt', 'w')
    f.write(str(dic))
    f.close()
    print(str(dic))

dataset = []
def loadVocabularyToMemory():
    for i in range(2):
        directory = 'english/' + vocabulary[i]
        doc = open(directory, 'r', encoding='UTF-8')
        
        for line in doc.readlines():
            data = json.loads(line)
            data = str(data).replace('$','')
            #print("data = " + data)
            dataset.append(data)
            
        print("i == " + str(i))
        

def loadDotCodeToMemory():
    for i in range(len(dotCode)):
        directory = 'dotCode/dotCode/' + dotCode[i]
        doc = open(directory, 'r')
        data = []
        for line in doc.readlines():
            data.append(json.loads(line))
    
personInfoDataset = {}
personIdDataset = []
def vocCountArrangeEachPerson():
    for i in range(len(dataset)):
        preData = {}
        datasetDict = eval(dataset[i])
        voc = datasetDict['_id']['vocabulary']
        preData.update( {"total" : datasetDict['total']} )
        preData.update( {"correct" : datasetDict['correct']} )
        preData.update( {"numberLong" : datasetDict['lastModified']['numberLong']} )
        data = {voc : preData}
        if datasetDict['_id']['userId'] in personInfoDataset.keys():
            personInfoDataset[datasetDict['_id']['userId']].update(data)
        else:
            personInfoDataset.update( {datasetDict['_id']['userId'] : data} )
            personIdDataset.append(datasetDict['_id']['userId'])
    
    #print(personInfoDataset[24643])

personInfoDatasetInOrder = []
def vocCountArrangeEachPersonInTimeSeries():
    
    personIdDataset.sort()
    for personIndex in range(len(personIdDataset)):
        numberLongList = []
        info = personInfoDataset[personIdDataset[personIndex]] 
        
        for key in info.keys():
            numberLongList.append(info[key]['numberLong'])
        
        numberLongList.sort()
        
        personInfoDatasetInOrderTemp = []

        for i in range(len(numberLongList)):
            for key in info.keys():
                if info[key]['numberLong'] == numberLongList[i]:
                    personInfoDatasetInOrderTemp.append({key : info[key]})
                    del info[key]
                    break
        personInfoDatasetInOrder.append(personIndex)
        personInfoDatasetInOrder.append(personInfoDatasetInOrderTemp)        



# TODO Finish the ranking difficulty func
"""
def difficultyDetect(volcabulary):
    length = len(volcabulary)
    # KKphoneticNum: the num of KK phonetic 
    # which level the volcabulary in GEPT
    dificulty = (length * 0.7 + KKphoneticNum * 0.3) / 100 * GEPTLevel

    return dificulty
"""

def main():
    loadVocabularyToMemory()
    vocCountArrangeEachPerson()
    vocCountArrangeEachPersonInTimeSeries()
    #loadDotCodeToMemory()

    
main()