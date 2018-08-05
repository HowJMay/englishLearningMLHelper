import pickle
import pprint

with open('vocGoogleSearch.txt', 'rb') as f:
    vocDictGoogleSearch = pickle.load(f)

pprint.pprint(vocDictGoogleSearch)

print('==================================================================================================')

with open('vocKK.txt', 'rb') as f:
        vocDictKK = pickle.load(f)
pprint.pprint(vocDictKK)