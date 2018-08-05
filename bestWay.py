import pickle

def findMaxPath(learningSlopeDict, allVocList):
    
    maxPathNode = -10.0
    originFormer = ''
    originLatter = ''

    for formerKey in allVocList:
        if formerKey in learningSlopeDict.keys():
            for latterKey in learningSlopeDict[formerKey].keys():
                if latterKey in allVocList:
                    # find the slope which owns the max value and uses it as origin to create a max value path tree
                    slope = float(learningSlopeDict[formerKey][latterKey]['slope'])
                    if slope > maxPathNode:
                        maxPathNode = slope
                        originFormer = formerKey
                        originLatter = latterKey
    if originFormer == '':
        return []
    else:
        allVocList.remove(originFormer)
        allVocList.remove(originLatter)
        path = [originFormer, originLatter]
        

        return path


def bestWay_Alorithm(learningSlopeDict):
    maxPathNode = 0.0
    originFormer = ''
    originLatter = ''

    allVocList = []
    for formerKey in learningSlopeDict.keys():
        for latterKey in learningSlopeDict[formerKey].keys():
            
            # create a list which contains all voc 
            if not formerKey in allVocList:
                allVocList.append(formerKey)

            # find the slope which owns the max value and uses it as origin to create a max value path tree
            slope = float(learningSlopeDict[formerKey][latterKey]['slope'])

            if slope > maxPathNode:
                maxPathNode = slope
                originFormer = formerKey
                originLatter = latterKey

    allVocList.remove(originFormer)
    allVocList.remove(originLatter)
    
    allPath = []
    path = [originFormer, originLatter]
    allPath.append(path)

    head = originFormer
    tail = originLatter

    while len(allVocList) > 0:
        maxPathNode = -100.0
        nextNodeFormerKey = ''
        nextNode = ''
        
        # find the max slope which current "head" and "tail" in path can reach 
        for formerKey in [head, tail]:
            for latterKey in learningSlopeDict[formerKey].keys():
                
                slope = float(learningSlopeDict[formerKey][latterKey]['slope'])
                
                print ('slope = {}, maxPathNode = {}, len(allVocList) = {}'.format(slope, maxPathNode, len(allVocList)))

                if (slope > maxPathNode) and (not (latterKey in path)) and (latterKey in allVocList):
                    maxPathNode = slope
                    nextNodeFormerKey = formerKey
                    nextNode = latterKey


        # if cant find any available node in this path. all other available path is on the other seperate path
        if nextNode == '':
            allPath.append(path)        
            path = findMaxPath(learningSlopeDict, allVocList)
            tail = nextNode
        else:
            allVocList.remove(nextNode)

        if nextNodeFormerKey == head:
            path.insert(0, nextNode)
            head = nextNode
        elif nextNodeFormerKey == tail:
            path.append(nextNode)
            tail = nextNode
    
    
    with open('path.txt', 'wb') as fp:
        fp.write(str(path))     

    return path

def al_algorithm(learningSlopeDict):
    allVocList = []
    for formerKey in learningSlopeDict.keys():
        # create a list which contains all voc 
        if not formerKey in allVocList:
            allVocList.append(formerKey)       

    # make a Dict which contains the relation between all the voc
    allDictList = []
    for formerKey in allVocList:
        for latterKey in allVocList:
            
            dic = {'formerKey' : formerKey, 'latterKey' : latterKey}

            if latterKey in learningSlopeDict[formerKey].keys():
                slope = float(learningSlopeDict[formerKey][latterKey]['slope'])
            else:
                slope = -10.0

            dic.update({'slope' : slope})
            allDictList.append(dic)
    

    # find the start point of the path 
    maxPathNode = 0.0
    maxDict = {}
    for dic in allDictList:
        slope = dic['slope']
        if slope > maxPathNode:
            maxPathNode = slope
            maxDict = dic
    
    allPath = []
    path = [maxDict['formerKey'], maxDict['latterKey']]
    allPath.append(path)

    head = maxDict['formerKey']
    tail = maxDict['latterKey']

    allDictList.remove(maxDict)

    while len(allDictList) > 0:
        maxPathSlope = -10.0
        maxDict= {}
        
        # find the max slope which current "head" and "tail" in path can reach 
        for formerKey in [head, tail]:
            for dic in allDictList:
                if formerKey == dic['formerKey']:
                    slope = dic['slope']

                if (slope > maxPathSlope) and (not (dic['latterKey'] in path)):
                    maxPathSlope = slope
                    maxDict = dic
        print ('maxDict = {}, len(allDictList) = {}'.format(maxDict, len(allDictList)))
        if maxDict in allDictList:
            allDictList.remove(maxDict)
        elif maxDict == {}:
            print('maxDict == {}')
            print(path)
        elif not maxDict in allDictList:
            print('not maxDict in allDictList')
            print(path)


        if maxDict['formerKey'] == head:
            path.insert(0, maxDict['latterKey'])
            head = maxDict['latterKey']
        elif maxDict['formerKey'] == tail:
            path.append(maxDict['latterKey'])
            tail = maxDict['latterKey']
    
    print (path)






    