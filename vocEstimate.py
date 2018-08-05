from pprint import pprint

import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras import backend as K

import pickle
import numpy as np

def removeSpaceInTheEnd(word):
    while word[len(word) - 1] == ' ':
        if len(word) == 1:
            return -1
        word = word[0:len(word) - 1]
        
    return word


def loadTxt():
    text = ""
    with open('./voc.txt', 'r') as f:
        allLines = f.readlines()
        for line in allLines:
            text  = text + line
    
    with open('./vocKK.txt', 'rb') as f:
        KKDict = pickle.load(f)

    with open('./vocGoogleSearch.txt', 'rb') as f:
        searchDict = pickle.load(f)
    
    for i in range(10):
        text = text.replace('('+str(i)+')', '')
        text = text.replace(str(i), '')
    text = text.replace(')', '')
    levelVocRaw = text.split('LEVEL')
    levelVocData = []
    for level_index in range(len(levelVocRaw)):
        vocs = levelVocRaw[level_index].split('\n')
        singleLevelData = []
        for voc in vocs:
            if voc != '' and voc != ' ':
                if '/' in voc:
                    voc_tempList = voc.split('/')
                    for voc_temp in voc_tempList:
                        if voc_temp != '':
                            voc_temp = removeSpaceInTheEnd(voc_temp)
                            if voc_temp == -1:
                                    continue
                            #KK = KKDict[voc_temp]
                            if voc_temp in searchDict:
                                vocSearchDict = searchDict[voc_temp]
                            leadingNum = vocSearchDict['leadingNum']
                            numDigit = vocSearchDict['numDigit'] 
                            #singleLevelData.append([voc_temp, KK, leadingNum, numDigit, level_index])
                            singleLevelData.append([voc_temp, leadingNum, numDigit, level_index])

                elif '(' in voc:
                    voc_tempList = voc.split('(')
                    voc_temp = removeSpaceInTheEnd(voc_tempList[0])
                    if voc_temp == -1:
                                continue
                    
                    #KK = KKDict[voc_temp]
                    if voc_temp in searchDict:
                        vocSearchDict = searchDict[voc_temp]
                    leadingNum = vocSearchDict['leadingNum']
                    numDigit = vocSearchDict['numDigit']
                    #singleLevelData.append([voc_temp, KK, leadingNum, numDigit, level_index])
                    singleLevelData.append([voc_temp, leadingNum, numDigit, level_index])
                    
                    voc_temp = removeSpaceInTheEnd(voc_tempList[1]) + voc_tempList[1]
                    if voc_temp == -1:
                                continue
                    #KK = KKDict[voc_temp]
                    if voc_temp in searchDict:
                        vocSearchDict = searchDict[voc_temp]
                    leadingNum = vocSearchDict['leadingNum']
                    numDigit = vocSearchDict['numDigit']
                    #singleLevelData.append([voc_temp, KK, leadingNum, numDigit, level_index])
                    singleLevelData.append([voc_temp, leadingNum, numDigit, level_index])
                else:
                    voc_temp = removeSpaceInTheEnd(voc)
                    if voc_temp == -1:
                                continue
                    #KK = KKDict[voc_temp]
                    if voc_temp in searchDict:
                        vocSearchDict = searchDict[voc_temp]
                    leadingNum = vocSearchDict['leadingNum']
                    numDigit = vocSearchDict['numDigit']
                    #singleLevelData.append([voc_temp, KK, leadingNum, numDigit, level_index])
                    singleLevelData.append([voc_temp, leadingNum, numDigit, level_index])

        if len(singleLevelData) > 0:
            levelVocData.append(singleLevelData)
            
    
    return levelVocData

    
charListLen = 58
def countCharNum(vocabulary):
    # charList = ['Capital'(26 elements), 'Lowercase'(26 elements), 'apostrophe', 'minus', 'space', 'point', '’', 'é']
    charList = []

    for i in range(charListLen):
        charList.append(0)

    for char in vocabulary:
        index = -1
        if 65 <= ord(char) and ord(char) <= 90:
            index = ord(char) - 65
        elif 97 <= ord(char) and ord(char) <= 122:
            index = ord(char) - 97 + 26 
        elif char == "'": 
            index = 52
        elif char == '-':
            index = 53
        elif char == ' ':
            index = 54
        elif char == '.':
            index = 55
        elif char == '’':
            index = 56
        elif char == 'é':
            index = 57

        if index != -1:
            charList[index] = charList[index] + 1
        else:
            print('vocabulary ===')
            print(vocabulary)

    for i in range(len(charList)):
        charList[i] = charList[i]/len(vocabulary)
    return charList
    
def getCharOrderList(vocabulary):
    vocCharOrderList = []

    for char in vocabulary:
        index = -1        
        if 65 <= ord(char) and ord(char) <= 90:
            index = ord(char) - 65
        elif 97 <= ord(char) and ord(char) <= 122:
            index = ord(char) - 97 + 26 
        elif char == "'": 
            index = 52
        elif char == '-':
            index = 53
        elif char == ' ':
            index = 54
        elif char == '.':
            index = 55
        elif char == '’':
            index = 56
        elif char == 'é':
            index = 57
            
        if index != -1:
            vocCharOrderList.append(index/(charListLen - 1))
        else:
            print('vocabulary ===')
            print(vocabulary)

    return vocCharOrderList
def countKKNum(KK):
    return len(KK)

def getCharCombinationList(vocabulary):
    vowelList = ['a', 'e', 'i', 'o', 'u']
    specialVowelList = ['ar', 'er', 'ir', 'or', 'ur', 'ou', 'ow' 'aw', 'ai', 'oi', 'ui', 'ay', 'ey', 'oy', 'ea', 'ee', 'oo', 'ie', 'igh', 'all', 'ell', 'ill', 'oa']
    consonantList = ['b', 'c', 'd', 'f', 'g', 'h', 'j', 'k', 'l', 'm', 'n', 'p', 'q', 'r', 's', 't', 'v', 'w', 'x', 'y', 'z']
    specialConsonantList = ['th', 'ti', 'sh', 'ch', 'wh', 'ph', 'ti', 'bl', 'cl', 'fl', 'sl', 'br', 'cr', 'dr', 'tr', 'sion', 'sure', 'ture', 'ssion', 'cian', 'kn', 'wr' ]
    
    if vocabulary[len(vocabulary) - 1] == 'e' and vocabulary[len(vocabulary) - 2] != 'e':
        vocabulary = vocabulary[0:len(vocabulary) - 1]
    
    vocCharCombinationList = vowelList + specialVowelList + specialConsonantList
    vocCharCombinationCountList = [0 for x in range(len(vowelList) + len(specialVowelList) + len(specialConsonantList))]
    
    for element_index in range(len(vocCharCombinationList)):
        vocCharCombinationCountList[element_index] = vocabulary.count(vocCharCombinationList[element_index])

    return vocCharCombinationCountList


def preprocess_word(levelVocData): 
    charNumList = []
    #vocCharOrderList = []
    vocCharCombinationCountList = []
    leadingNumList = []
    numDigitList = []
    targetList = []

    for levelData in levelVocData:
        for vocData in levelData:
            vocabulary = vocData[0]
            leadingNum = vocData[1]
            numDigit = vocData[2]
            target = vocData[3] - 1 # since a var y in range 0 - 9 will become a vector whose length is 10 with keras.utils.to_categorical 
            """ the old one
            KK = vocData[1]
            leadingNum = vocData[2]
            numDigit = vocData[3]
            target = vocData[4] - 1 # since a var y in range 0 - 9 will become a vector whose length is 10 with keras.utils.to_categorical 
            """
            charNumList.append(countCharNum(vocabulary))
            #vocCharOrderList.append(getCharOrderList(vocabulary))
            vocCharCombinationCountList.append(getCharCombinationList(vocabulary))
            leadingNumList.append(leadingNum)
            numDigitList.append(numDigit)
            targetList.append(target)

    return [charNumList, vocCharCombinationCountList, leadingNumList, numDigitList, targetList]

    
def getDataset(charNumList, vocCharCombinationCountList, leadingNumList, numDigitList, targetList):
    
    train_index = [3, 4, 7]
    test_index = 6
    x_train = []
    y_train = []
    x_test =[]
    y_test = []
    for i in range(len(charNumList)):
    
        if i%10 in train_index:
            x_train.append([charNumList[i] + vocCharCombinationCountList[i] + leadingNumList[i] + numDigitList[i]])
            y_train.append(targetList[i])
        elif i%10 == test_index:
            x_test.append([charNumList[i] + vocCharCombinationCountList[i] + leadingNumList[i] + numDigitList[i]])
            y_test.append(targetList[i])        

    return [x_train, y_train, x_test, y_test]

def NN(x_train_raw, y_train_raw, x_test_raw, y_test_raw):
    batch_size = 128
    num_classes = 6
    epochs = 12

    x_train = np.asarray(x_train_raw)
    x_test = np.asarray(x_test_raw)
    y_train = np.asarray(y_train_raw)
    y_test = np.asarray(y_test_raw)

    x_train = x_train.astype('float32')
    x_test = x_test.astype('float32')

    y_train = keras.utils.to_categorical(y_train, num_classes)
    y_test = keras.utils.to_categorical(y_test, num_classes)
    
    model = Sequential()
    model.add(Dense(32, input_dim = 107))
    model.add(Dropout(0.25))
    model.add(Dense(128, activation='relu'))
    model.add(Dropout(0.5))
    model.add(Dense(num_classes, activation='softmax'))

    model.compile(loss=keras.losses.categorical_crossentropy,
              optimizer=keras.optimizers.Adadelta(),
              metrics=['accuracy'])
    model.fit(x_train, y_train,
          batch_size=batch_size,
          epochs=epochs,
          verbose=1,
          validation_data=(x_test, y_test))
    score = model.evaluate(x_test, y_test, verbose=0)
    print('Test loss:', score[0])
    print('Test accuracy:', score[1])

    return 'result'
    


def main():
    #logging.basicConfig(level=logging.DEBUG)
    
    levelVocData = loadTxt()
    
    [charNumList, vocCharCombinationCountList, leadingNumList, numDigitList, targetList] = preprocess_word(levelVocData)

    x_train, y_train, x_test, y_test = getDataset(charNumList, vocCharCombinationCountList, leadingNumList, numDigitList, targetList)
    NN(x_train, y_train, x_test, y_test)


main()