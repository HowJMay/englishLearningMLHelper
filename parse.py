import numpy as np
import sklearn.linear_model as LinearRegressionResult
import math
import pickle
import bestWay

def loadTxtCalculationFactor():
    f = open('LinearRegressionResult.txt', 'r', encoding = 'UTF-8')

    text = ''
    while True:
        data = f.readline()
        if data == '':
            break
        text = text + data

    f.close()

    text = text.replace('array', '')
    text = text.replace('(', '')
    text = text.replace(')', '')
    text = text.replace('[', '')
    text = text.replace(']', '')
    text = text.replace(' ', '')

    textList = text.split(',')
    return textList

def saveTxtCalculationFactor(text):
    f = open("LRResult.txt", 'w', encoding = 'UTF-8')
    f.write(str(text))

numTextList = []
absTextList = []
def calculationFactor(textList):
    for i in range(len(textList)):
        preNum = textList[i].split('e')
        
        base = 0
        power = 0
        if len(preNum) == 2:
            base = float(preNum[0])
            power = int(preNum[1])
        else:
            base = float(preNum[0])
            power = 0
        num = float(base) * pow(10, int(power))
        numTextList.append(num) 
        absTextList.append(abs(numTextList[i]))
def calculationFactorProcess():
    textList = loadTxtCalculationFactor()
    calculationFactor(textList)
    print('max = ' + str(max(numTextList)))
    print('min = ' + str(min(numTextList)))
    print('abs max = ' + str(max(absTextList)))
    print('abs min = ' + str(min(absTextList)))
    print('mean = ' + str(np.mean(np.asarray(numTextList))))
    print('abs mean = ' + str(np.mean(np.asarray(absTextList))))
    print('std = ' + str(np.std(np.asarray(numTextList))))
    print('abs std = ' + str(np.std(np.asarray(absTextList))))
    saveTxtCalculationFactor(textList)

def loadTxtBestWay():
    text = []
    for i in range(11):
        fileName = 'personInfoDatasetInOrder' + str(i) + '.txt'
        with open(fileName, 'rb') as f:
            tempList = pickle.load(f)
        for elementList in tempList:
            text.append(elementList)
    return text

def arrangePersonInfoList(textList):
    personInfoList = []
    for i in range(1, len(textList), 2):
        personInfoList.append(textList[i])

    return personInfoList
    
def learningSlopeCal(personInfoList):
    learningSlopeDict = {}

    for personIndex in range(len(personInfoList)):
        personVocHist = personInfoList[personIndex]
        for vocIndex in range(0, len(personVocHist) - 1):
            
            formerVocAsDict = personVocHist[vocIndex]
            latterVocAsDict = personVocHist[vocIndex + 1]
            
            formerKey = next(iter(formerVocAsDict))
            latterKey = next(iter(latterVocAsDict))

            formerValue = formerVocAsDict[formerKey]
            latterValue = latterVocAsDict[latterKey]

            if not formerKey in learningSlopeDict.keys(): 
                # the former key didnt exist in the dict
                slope = int(latterValue['correct']) /int(latterValue['total'])  - int(formerValue['correct']) /int(formerValue['total']) 

                valueDict = {latterKey : {'slope' : slope} }
                learningSlopeChildDict = {formerKey : valueDict}
                learningSlopeDict.update(learningSlopeChildDict)
            elif not latterKey in learningSlopeDict[formerKey].keys(): 
                # the former key exists in the dict but latter key didnt exist in the dict
                slope = int(latterValue['correct']) /int(latterValue['total'])  - int(formerValue['correct']) /int(formerValue['total']) 

                valueDict = {latterKey : {'slope' : slope} }
                learningSlopeDict[formerKey].update(valueDict)
            else:
                # both former and latter key didnt exist in the dict
                preSlope = learningSlopeDict[formerKey].pop(latterKey)['slope']
                curSlope = int(latterValue['correct']) /int(latterValue['total'])  - int(formerValue['correct']) /int(formerValue['total']) 

                slope = (preSlope + curSlope) / 2
                valueDict = {latterKey : {'slope' : slope} }
                learningSlopeDict[formerKey].update(valueDict)
    return learningSlopeDict   



def calculationBestWayProcess():
    text = loadTxtBestWay()
    personInfoList = arrangePersonInfoList(text)

    learningSlopeDict = learningSlopeCal(personInfoList)
    bestWay.bestWay_Alorithm(learningSlopeDict)

def main():
    calculationBestWayProcess()




main()
