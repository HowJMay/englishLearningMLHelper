import requests
from bs4 import BeautifulSoup



vocDictKK = {}

def importVoc():
    f = open('vocAll.txt', 'r', encoding = 'UTF-8')
    vocStr = ""
    while True:
        tempStr = f.readline()
        if tempStr == '':
            break
        vocStr = vocStr + tempStr
    
    vocStr = vocStr.replace('\'', '')
    vocStr = vocStr.replace('[', '')
    vocStr = vocStr.replace(']', '')
    vocList = vocStr.split(',')
    
    return vocList


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
    else:
        resKK = ""
    resKK = resKK.replace('[', '')
    resKK = resKK.replace(']', '')
    resKK = resKK.replace('KK', '')

    
    return resKK

def getKKforEachVoc(vocList):
    for i in range(len(vocList)):
        text = getHtml(vocList[i])
        KK = parseHTMLForKK(text)
        vocDictKK.update({vocList[i] : KK})

def main():
    vocList = importVoc()
    getKKforEachVoc(vocList)

    print(vocDictKK)
main()


