'''
NOTES:

invertedIndex = {
    'token' : {
        '0/10' : 10,
        '42/81': 4,
        '3/231': 61,
        '3/11: 11,
    },
    ...
}


returnedInvertedIndex = {
    'token' : {
        idf: 11.31,
        high: {
            '0/10' : 4.31,
            '42/81': 6.11,
            '3/231': 9.11,
        },
        low: {
            '3/11': 3.21,
            '4/44': 0.14
        }
    },
    ...
}

Methods to Use:
1. Index Elimination
    - High-idf query terms only (catcher in the rye => catcher, rye)
    - Only look at documents with at least half high-idf query words, 2 out of 4
2. High and Low Lists
    - If >2.5 TF-IDF => high
    - Else => low
3. Total term frequency for document = sum of term frequency for each term
'''

from bs4 import BeautifulSoup
import pickle
from nltk import word_tokenize, sent_tokenize
from nltk.tokenize import ToktokTokenizer
from math import log10

from collections import defaultdict

def dd():
    return defaultdict(int)

def main():
    invertedIndex = defaultdict(dd)

    absolute = 'WEBPAGES_RAW/'

    bookkeepingFile = open(absolute + 'bookkeeping.tsv', 'r')

    numDocs = 0

    for line in bookkeepingFile.readlines():
        lineSplit = line.split()
        filePath = lineSplit[0]
        fileURL = lineSplit[1]

        htmlFile = open(absolute + filePath, 'r')

        soup = BeautifulSoup(htmlFile.read(), 'html.parser')

        for script in soup(['script', 'style']):
            script.decompose()

        text = soup.get_text().lower()

        tokenizer = ToktokTokenizer()

        tokens = [ sentToken for sentence in sent_tokenize(text) for sentToken in tokenizer.tokenize(sentence) if sentToken.strip() and len(sentToken) > 1 ]

        for token in tokens:
            invertedIndex[token][filePath] += 1

        numDocs += 1

        print('--' + str(numDocs) + '--')

        htmlFile.close()

    print('----INVERTED INDEX CREATED----')

    for token in invertedIndex:

        idf = log10(numDocs / len(invertedIndex[token]))

        high = {}
        low = {}

        for docFilePath in invertedIndex[token]:
            termFrequency = invertedIndex[token][docFilePath]
            tf = 1 + log10(termFrequency)

            tfidf = tf * idf

            if tfidf > 2:
                high[docFilePath] = tfidf
            else:
                low[docFilePath] = tfidf

        invertedIndex[token] = {}

        invertedIndex[token]['idf'] = idf
        invertedIndex[token]['high']= high
        invertedIndex[token]['low'] = low



    pickleDict = open("dict.pickle", "wb")
    pickle.dump(invertedIndex, pickleDict)

    bookkeepingFile.close()
    pickleDict.close()

main()
