import requests
from bs4 import BeautifulSoup
import pickle
import time

vocDictKK = {}
vocDictGoogleSearch = {}

def importVoc():
    text = ""
    with open('./voc.txt', 'r') as f:
        allLines = f.readlines()
        for line in allLines:
            text  = text + line

    vocList = text.replace('LEVEL\n', '')
    
    tempList = []
    vocs = vocList.split('\n')

    for voc in vocs:
        if voc != None:
            if '/' in voc:
                temp = voc.split('/')
                for t in temp:
                    tempList.append(t)
            elif '(' in voc:
                voc = voc.replace(')', '')
                v = voc.split('(')
                tempList.append(v[0])
                vv = v[0] + v[1]
                tempList.append(vv)
            else:
                tempList.append(voc)
        
    print(len(tempList))
    return tempList

def getHtml(voc):
    yahooDicSearchURL = "https://tw.dictionary.search.yahoo.com/search?p="
    url = yahooDicSearchURL + str(voc)
    r = requests.get(url)


    return r.text
    
def parseHTMLForKK(text):
    soup = BeautifulSoup(text, 'html.parser')
    soup1st = soup.find('li', class_ = 'd-ib mr-10 va-top')
    if soup1st != None:
        resKK = soup1st.find('span').contents[0]
        resKK = resKK.replace('[', '')
        resKK = resKK.replace(']', '')
        resKK = resKK.replace('KK', '')
        resKK = resKK.replace(' ', '')
    else:
        resKK = None
    
    return resKK

def getKKforEachVoc(vocList):
    for i in range(len(vocList)):
        text = getHtml(vocList[i])
        KK = parseHTMLForKK(text)

        if KK == None or KK == "":
            print('None, ' + vocList[i])
        else:
            vocDictKK.update({vocList[i] : KK})
            time.sleep(1)
            print(vocList[i])
            print(time.time())
            
    with open('vocKK.txt', 'wb') as f:
        pickle.dump(vocDictKK, f)


def getHtmlFromGoogle(voc):
    googleSearchURL = "https://www.google.com.tw/search?q="
    url = googleSearchURL + str(voc)
    r = requests.get(url)

    return r.text

def parseHTMLForGoogle(text):
    soup = BeautifulSoup(text, 'html.parser')
    soupResult = soup.find(id = 'resultStats')
    if soupResult == None or soupResult == "":
        return None
    resultMessyStr = soupResult.contents[0]
    resultStr = (resultMessyStr.split(' ')[1]).replace(',', '')
    
    return resultStr
def getGoogleResultNum(vocList):    
    for voc in vocList:
        text = getHtmlFromGoogle(voc)

        if text == None or text == "":
            break
        else:
            searchResultStr = parseHTMLForGoogle(text)
            print(searchResultStr)
            if searchResultStr != None:
                vocDictGoogleSearch.update({voc : {'leadingNum' : int(searchResultStr[0]), 'numDigit' : len(searchResultStr)}})

                time.sleep(1)
                print(time.time()) 
    with open('vocGoogleSearch.txt', 'wb') as f:
        pickle.dump(vocDictGoogleSearch, f)


def main():
    
    vocList = importVoc()
    getKKforEachVoc(vocList)
    #getGoogleResultNum(vocList)
    
    return vocDictKK

main()