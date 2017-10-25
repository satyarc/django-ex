import os
from django.shortcuts import render
from django.conf import settings
from django.http import HttpResponse
from . import database
import spacy
import en_core_web_sm
import json
import requests
from collections import Counter
import nsepy as nsp

noisy_pos_tags = ["PROP","DET","PART","CCONJ","ADP","PRON","VERB","ADJ"]
min_token_length = 2

def isNoise(token):     
    is_noise = False
    if token.pos_ in noisy_pos_tags: 
        is_noise = True 
    elif token.is_stop == True:
        is_noise = True
    elif len(token.string) <= min_token_length:
        is_noise = True
    return is_noise 

def cleanup(token, lower = True):
    if lower:
       token = token.lower()
    return token.strip()

   
def fetchNewsFrom(newsSource):
    apiKey = 'a892420deb3f46dea3c5f5c0b9863bf3'
    url = "https://newsapi.org/v1/articles?apiKey=" + apiKey + "&source=" + newsSource
    response = requests.get(url)
    data = response.json()
    docFromSource = ""

    if data["status"] != "error":
        articles = data["articles"]
        for article in articles:
            if article["description"] is not None:
                description = article["description"]
                docFromSource += description
    else:
        print("Invalid news source.")
    return docFromSource
    

def fetchNewsFromSources():
    url = "https://newsapi.org/v1/sources?language=en&category=business"
    response = requests.get(url)
    data = response.json()
    docFromSources = ""
    
    if data["status"] != "error":
        sources = data["sources"]
        for source in sources:
            docFromSources += fetchNewsFrom(source["id"])
    else:
        print("Invalid news source.")
        
    return docFromSources

# Create your views here.
'''
def index(request):
    nlp = en_core_web_sm.load()               
    doc = nlp(fetchNewsFromSources())             
    cleaned_list = [cleanup(word.string) for word in doc if not isNoise(word)]
    return render(request, 'welcome/index.html', {
        'listOfWords': cleaned_list
    })
'''
def index(request):
    data = nsp.get_history(symbol = trade_name, start = date.today(),end = date.today())
    return render(request, 'welcome/index.html', {
        'Closing': data.Close
    })

def health(request):
    return HttpResponse(PageView.objects.count())
