import pickle

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
            if not latterKey in allVocList:
                allVocList.append(latterKey)


            # find the slope which owns the max value and uses it as origin to create a max value path tree
            slope = float(learningSlopeDict[formerKey][latterKey]['slope'])
            if slope > maxPathNode:
                maxPathNode = slope
                originFormer = formerKey
                originLatter = latterKey

    allVocList.remove(originFormer)
    allVocList.remove(originLatter)
    path = [originFormer, originLatter]
    
    head = originFormer
    tail = originLatter

    while len(allVocList) > 0:
        maxPathNode = 0.0
        nextNodeFormerKey = ''
        nextNode = ''
        
        # find the max slope which current "head" and "tail" in path can reach 
        for formerKey in [head, tail]:
            for latterKey in learningSlopeDict[formerKey].keys():
                
                slope = float(learningSlopeDict[formerKey][latterKey]['slope'])

                if (slope > maxPathNode) and (not (latterKey in path)):
                    maxPathNode = slope
                    nextNodeFormerKey = formerKey
                    nextNode = latterKey
        
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

        



