from pprint import pprint

import keras
from keras.models import Sequential
from keras.layers import Dense, Dropout, Flatten
from keras import backend as K

import pickle
import numpy as np



def loadTxt():
    text = ""
    with open('./vocTemp.txt', 'r') as f:
        allLines = f.readlines()
        for line in allLines:
            text  = text + line
    
    with open('./vocKK.txt', 'rb') as f:
        KKDict = pickle.load(f)

    with open('./vocvocGoogleSearch.txt', 'rb') as f:
        searchDict = pickle.load(f)
    
    for i in range(10):
        text = text.replace('('+str(i)+')', '')
        text = text.replace(str(i), '')
    text = text.replace(')', '')
    levelVocRaw = text.split('LEVEL')
    levelVocData = []
    for level_index in range(len(levelVocTemp)):
        vocs = levelVocTemp[level_index].split('\n')
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
                            KK = KKDict[voc_temp]
                            vocSearchDict = searchDict[voc_temp]
                            leadingNum = vocSearchDict['leadingNum']
                            numDigit = vocSearchDict['numDigit'] 
                            singleLevelData.append([voc_temp, KK, leadingNum, numDigit])

                elif '(' in voc:
                    voc_tempList = voc.split('(')
                    voc_temp = removeSpaceInTheEnd(voc_tempList[0])
                    if voc_temp == -1:
                                continue
                    
                    KK = KKDict[voc_temp]
                    vocSearchDict = searchDict[voc_temp]
                    leadingNum = vocSearchDict['leadingNum']
                    numDigit = vocSearchDict['numDigit']
                    singleLevelData.append([voc_temp, KK, leadingNum, numDigit])
                    
                    
                    voc_temp = removeSpaceInTheEnd(voc_tempList[1]) + voc_tempList[1]
                    if voc_temp == -1:
                                continue
                    KK = KKDict[voc_temp]
                    vocSearchDict = searchDict[voc_temp]
                    leadingNum = vocSearchDict['leadingNum']
                    numDigit = vocSearchDict['numDigit']
                    singleLevelData.append([voc_temp, KK, leadingNum, numDigit])

                else:
                    voc_temp = removeSpaceInTheEnd(voc)
                    if voc_temp == -1:
                                continue
                    KK = KKDict[voc_temp]
                    vocSearchDict = searchDict[voc_temp]
                    leadingNum = vocSearchDict['leadingNum']
                    numDigit = vocSearchDict['numDigit']
                    singleLevelData.append([voc_temp, KK, leadingNum, numDigit])
        
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

processedDataList = []
targetList = []
def preprocess_singleWord(levelVocData): 
        for vocData in levelVocData:
            vocabulary = vocData[0]
            KK = vocData[1]
            searchLeadingNum = vocData[2]
            searchNumDigit = vocData[3]
            
            target = vocData[4] 
            
            charNumList = countCharNum(vocabulary)
            KKNum = countKKNum(KK)
            


            processedData = []
            for char in charNumList:
                processedData.append(char)
            processedData.append(KKNum)
            processedData.append(searchLeadingNum)
            processedData.append(searchNumDigit)
            processedDataList.append(processedData)

            targetList.append(target)
            
        processedDataSort = []
        targetSort = []
        for i in range(10):
            processedDataSort.append([])
            targetSort.append([])
        for i in range(len(processedDataList)):
            processedDataSort[i % 10].append(processedDataList[i])
            targetSort[i % 10].append(targetList[i])
        with open('./x_dataSortForTarin.txt', 'wb') as f:
            pickle.dump(f, processedDataSort)

        with open('./y_dataSortForTarin.txt', 'wb') as f:
            pickle.dump(f, targetSort)


        processedDataListNpArray = np.asarray(processedDataSort[0])
        tagetListNpArray = np.asarray(targetSort[0])
        

        return [processedDataListNpArray, tagetListNpArray]
    


def preprocess_word(levelVocData): 
    charNumList = []
    vocCharOrderList = []
    targetList = []

    for levelData in levelVocData:
        for vocData in levelData:
            vocabulary = vocData[0]
            target = vocData[1]

            charNumList.append(countCharNum(vocabulary))
            vocCharOrderList.append(getCharOrderList(vocabulary))
            targetList.append(target)

    return [charNumList, vocCharOrderList, targetList]

    
def getDataset(charNumList, vocCharOrderList, targetList):
    
    train_index = 3
    x_train = []
    y_train = []
    x_test =[]
    y_test = []
    
    for i in range(len(charNumList)):
        if i%10 == train_index:
            x_train.append([charNumList[i], vocCharOrderList[i]])
            y_train.append(targetList[i])        
        else:
            x_test.append([charNumList[i], vocCharOrderList[i]])
            y_test.append(targetList[i])        

    return [x_train, y_train, x_test, y_test]

def NN(x_train, y_train, x_test, y_test):
    batch_size = 128
    num_classes = 6
    epochs = 12

    x_train = x_train.astype('float32')
    x_test = x_test.astype('float32')
    x_train /= 255
    x_test /= 255
    print('x_train shape:', x_train.shape)
    print(x_train.shape[0], 'train samples')
    print(x_test.shape[0], 'test samples')


    # convert class vectors to binary class matrices
    y_train = keras.utils.to_categorical(y_train, num_classes)
    y_test = keras.utils.to_categorical(y_test, num_classes)

    model = Sequential()

    model.add(Dense(128, activation='relu', input_shape=()))
    model.add(Dense(256, activation='relu'))
    model.add(Dense(128, activation='relu'))
    
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
    


def main():
    levelVocData = loadTxt()

    [charNumList, vocCharOrderList, targetList] = preprocess_word(levelVocData)

    x_train, y_train, x_test, y_test = getDataset(charNumList, vocCharOrderList, targetList)
    NN(x_train, y_train, x_test, y_test)


main()