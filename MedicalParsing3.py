import re
import linkGrabber
import requests
from bs4 import BeautifulSoup
import time
import pickle
import pandas as pd
import nltk
import threading, random
# nltk.download()
import textblob
import numpy as np
from nltk.tokenize import sent_tokenize, word_tokenize
from nltk.tokenize import TweetTokenizer
from nltk.corpus import stopwords
from nltk.corpus import state_union
from nltk.tokenize import PunktSentenceTokenizer
from nltk.corpus import wordnet
from textblob.classifiers import NaiveBayesClassifier
from textblob import TextBlob
from nltk.corpus import movie_reviews
import matplotlib.pyplot as plt
import statistics
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import httplib2

csv_file = r"MedicalContentTemp.csv"


def find_between(s, first, last):
    try:
        start = s.index(first)
        end = s.index(last, start) + len(last)
        return s[start:end]
    except ValueError:
        return ""


names1 = ['ORMid', 'Specialty', 'City', 'State', 'Country']
dframe1 = pd.read_excel("ORM Automation Stage One.xlsx", sheet_name="Input Sheet", names=names1)
print(dframe1)
listnames = []
listnames3 = []
listrating = []
listrating2 = []
listwebsite = []
listORM = []
linkReq = ''
z = 0
for index1, row1 in dframe1.iterrows():
    z += 1
    doctype = row1['Specialty']
    city = row1['City']
    state = row1['State']
    ORMid = row1['ORMid']
    doc = []
    doc = doctype.split()
    print("doc")
    print(doc)
    j = ""
    if len(doc) > 1:
        for i in doc:
            if len(j) > 0:
                j = j + "+" + i
            else:
                j = i
    else:
        j = doctype
    search = 'top+' + j + '+in+' + city + '+' + state
    url = 'https://www.google.com/search?q='
    # url='https://www.google.com/maps/search/'
    frame = pd.DataFrame()
    # links = linkGrabber.Links('https://www.google.co.in/maps/search/'+search)
    singlelink = url + search
    response = requests.get(singlelink, allow_redirects=True)
    p = response.content
    f1 = open("page.html", "w")
    f1.write(str(p))
    f2 = open("page.html", "r")
    x = f2.read()
    f1.close()
    print(
        '***************************************************************************************************************************')
    print(x)
    soup = BeautifulSoup(x, features="lxml")
    f2.close()
    print(
        '***************************************************************************************************************************')

    # search=search+"&np"
    # print("!!search!!")
    # print(search)
    search = search + "&rlst"
    for link in soup.select("a"):
        if (search in link['href']):
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~LINK~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            print(search)
            print(link['href'])
            linkReq = link['href']

    TARGET_LINK = linkReq.replace("ie=UTF-8&", "")
    print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~TARGET LINK~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
    print(TARGET_LINK)
    response = requests.get(TARGET_LINK, allow_redirects=True)
    p = response.content
    # print(p)
    f1 = open("page2.html", "w")
    f1.write(str(p))
    f2 = open("page2.html", "r")
    x2 = f2.read()
    # print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@ page 2 @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    # print(x2)
    f1.close()

    # print('***************************************************************************************************************************')

    soup2 = BeautifulSoup(x2, features="lxml")
    # Extracting all the <a> tags into a list.
    # print(soup2)
    j = 0
    listrating = []
    for i in soup2.select("div.deIvCb"):
        print("~~~~~~~NAME OF MEDICAL ORG~~~~~~~~~")
        print(i.text)
        listORM.append(ORMid)
        listnames.append(i.text)

        listrating.append("NA")
        n = i.text.split()
        print("~~~~~~~SPLITED NAME OF MEDICAL ORG~~~~~~~~~")
        print(n)
        MedWord = ''
        for m in n:
            regex = re.compile('[@_!#$%^&*()<>?/\|}{~:]')
            if (regex.search(m) == None):
                MedWord = MedWord + '+' + m
            else:
                continue
        print("~~~~~~~~~~~~~~~MED WORD~~~~~~~~~~~~~~")
        print(MedWord[1:])
        singlelink = url + MedWord + '+' + city
        print("~~~~~~~~~~~~~LINK FOR ONE PERTICULAR MED WORD ORG~~~~~~~~~~~~~~``")
        print(singlelink)
        print(
            "##########################################################################################################")
        response = requests.get(singlelink, allow_redirects=True)
        p = response.text
        f1 = open("page3.html", "w")
        f1.write(str(p))
        f2 = open("page3.html", "r")
        x = f2.read()
        f1.close()
        soup4 = BeautifulSoup(x, features="lxml")

        for link in soup4.select("div.uUPGi > div"):
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~LINK~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~")
            # print(link['href'])
            print(link)

            for k in link.select("a"):
                linkReq = k['href']
                print("FINAL LINK")
                print(linkReq)

            MedicalSiteLink = linkReq.replace("/url?q=", "")
            # print(MedicalSiteLink)
            if (
                    "http://www.com" in MedicalSiteLink or "google" in MedicalSiteLink or "https://www.com" in MedicalSiteLink):
                listwebsite.append("https://www.healthgrad.com/")
            elif (".com" in MedicalSiteLink):
                head, sep, tail = MedicalSiteLink.partition('.com')
                head = head + ".com"
                print(head)
                if (("facebook" in head) or ("wikipedia" in head) or ("yelp" in head)):
                    listwebsite.append("NA")
                else:
                    listwebsite.append(head)
                break
            elif (".org" in MedicalSiteLink):
                head, sep, tail = MedicalSiteLink.partition('.org')
                head = head + ".org"
                print(head)
                if (("facebook" in head) or ("wikipedia" in head) or ("yelp" in head)):
                    listwebsite.append("NA")
                else:
                    listwebsite.append(head)
                break
            elif (".net" in MedicalSiteLink):
                head, sep, tail = MedicalSiteLink.partition('.net')
                head = head + ".net"
                print(head)
                if (("facebook" in head) or ("wikipedia" in head) or ("yelp" in head)):
                    listwebsite.append("NA")
                else:
                    listwebsite.append(head)
                break
            elif (".edu" in MedicalSiteLink):
                head, sep, tail = MedicalSiteLink.partition('.edu')
                head = head + ".edu"
                print(head)
                if (("facebook" in head) or ("wikipedia" in head) or ("yelp" in head)):
                    listwebsite.append("NA")
                else:
                    listwebsite.append(head)
                break
            elif (".us" in MedicalSiteLink):
                head, sep, tail = MedicalSiteLink.partition('.us')
                head = head + ".us"
                print(head)
                if (("facebook" in head) or ("wikipedia" in head) or ("yelp" in head)):
                    listwebsite.append("NA")
                else:
                    listwebsite.append(head)
                break

    # j=j+1

    # if(j==4):
    #	break

    m = len(listrating)
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    print(m)

    k = 0

    for i in soup2.select("span.oqSTJd"):
        # print(i.text)
        k = k + 1
        listrating2.append(i.text)

    while (k < m):
        listrating2.append("NA")
        k = k + 1

    print(listORM)
    print(listnames)
    print(listrating2)
    print(listwebsite)
    df0 = pd.DataFrame({'ORMid': listORM})
    print (df0)
    df1 = pd.DataFrame({'Name': listnames})
    print (df1)
    df2 = pd.DataFrame({'Rating': listrating2})
    print (df2)
    df3 = pd.DataFrame({'Website': listwebsite})
    print (df3)

    df_new = pd.concat([df0, df1, df2, df3], axis=1)
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    print(df_new)
    if (z == 10):
        break

# df_new.to_csv(csv_file)

