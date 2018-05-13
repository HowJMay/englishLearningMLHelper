import numpy as np
import sklearn.linear_model as LinearRegressionResult
import math

def loadTxt():
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

def saveTxt(text):
    f = open("LRResult.txt", 'w', encoding = 'UTF-8')
    f.write(str(text))

numTextList = []
absTextList = []
def calculation(textList):
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
def main():
    textList = loadTxt()
    calculation(textList)
    print('max = ' + str(max(numTextList)))
    print('min = ' + str(min(numTextList)))
    print('abs max = ' + str(max(absTextList)))
    print('abs min = ' + str(min(absTextList)))
    print('mean = ' + str(np.mean(np.asarray(numTextList))))
    print('abs mean = ' + str(np.mean(np.asarray(absTextList))))
    print('std = ' + str(np.std(np.asarray(numTextList))))
    print('abs std = ' + str(np.std(np.asarray(absTextList))))
    saveTxt(textList)

main()
