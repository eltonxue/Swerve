from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.conf import settings

import json
import pickle
from operator import itemgetter
from nltk.tokenize import ToktokTokenizer
from collections import defaultdict

'''
Search Algorithm:
1. Loop through high-idf terms in query
2. Loop through high list of those high-idf terms
2. Append files and their tfidf and tf to output_links
3. Increase totaltfidf as you loop
4. If less than 10 files in output_links, loop through low list
5. Sort top 10 by totaltfidf
output_links = {
    '0/10' : 'totaltfidf',
    '1/413' : 'totaltfidf',
    '31/113' : 'totaltfidf',
    ...
}
'''

# Elton Xue 52611936
# Chanun Sumphanphaisal 25051704
# Project Group 159

import os.path

# Create your views here.
invertedIndex = {}
jsonData = {}

def load(request):
    global invertedIndex
    global jsonData

    BASE = os.path.dirname(os.path.abspath(__file__))

    pickleDict = open(os.path.join(BASE, "dict.pickle"), 'rb')

    pickleDictData = pickleDict.read()

    invertedIndex = pickle.loads(pickleDictData)

    jsonFile = open(os.path.join(BASE, "bookkeeping.json"), 'r')
    jsonString = jsonFile.read()

    jsonData = json.loads(jsonString)

    pickleDict.close()
    jsonFile.close()

    return JsonResponse({ 'success': True})

def index(request):
    global invertedIndex
    global jsonData

    output_links = []
    searchTermsReq = request.GET.get('term', '')

    print(searchTermsReq)

    tokenizer = ToktokTokenizer()

    searchTerms = tokenizer.tokenize(searchTermsReq)

    print(searchTerms)

    response = {}

    output_data = defaultdict(int)
    output_links = []

    for token in searchTerms:
        token = token.lower()
        if invertedIndex[token]['idf'] > 0.25 and len(token) > 1:
            print('Looking through high for: ' + token)
            for docFilePath in invertedIndex[token]['high']:
                tfidf = invertedIndex[token]['high'][docFilePath]
                output_data[docFilePath] += tfidf


    if (len(output_data) < 10):
        for token in searchTerms:
            token = token.lower()
            if invertedIndex[token]['idf'] > 0.25 and len(token) > 1:
                print('Looking through low for: ' + token)
                for docFilePath in invertedIndex[token]['low']:
                    tfidf = invertedIndex[token]['low'][docFilePath]
                    output_data[docFilePath] += tfidf

    output_data = sorted(output_data.items(), key=itemgetter(1), reverse = True)

    for docFilePath, tfidf in output_data[:10]:
        output_links.append((jsonData[docFilePath], tfidf))

    output_links.sort(key=itemgetter(1), reverse = True)

    response['term'] = searchTermsReq
    response['results'] = output_links
    response['totalURLs'] = len(output_data)
    response['uniqueTokens'] = len(invertedIndex)
    response['totalDocuments'] = len(jsonData)

    return JsonResponse(response)
