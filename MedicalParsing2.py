import re
import linkGrabber
import requests
from bs4 import BeautifulSoup
import time
import pickle
import pandas as pd
import nltk
import threading, random
#nltk.download()
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

csv_file = r"MedicalReviews.csv"
names1=['MEDid','ORMid','Name','Rating','Website'] 
dframe1=pd.read_excel("MedicalContent.xlsx",sheet_name="MedicalContent",names=names1)
print(dframe1)


ListReviews=[]
MEDID=[]
linkReq=""

for index1,row1 in dframe1.iterrows():
	if(index1==100):
		break
	MedicalPl=row1['Name']
	ID=row1["MEDid"]
	City="Atlanta"
	print(MedicalPl)
	n=MedicalPl.split()
	print(n)
	MedWord=''
	for m in n:
		MedWord=MedWord+'+'+m
	MedWord=MedWord+'+'+City	
	url='https://www.google.com/search?q='

	#url='https://www.google.com/maps/search/' 
	frame = pd.DataFrame()
	MedWord=MedWord.replace("&","")
	print("medword-------------->")
	print(MedWord)
	#links = linkGrabber.Links('https://www.google.co.in/maps/search/'+search)
	singlelink=url+MedWord[1:]+"+reviews+on+yelp.com"
	print(singlelink)
	response=requests.get(singlelink, allow_redirects=True)
	p=response.content
	f1=open("page4.html","w")
	f1.write(str(p))
	f2=open("page4.html","r")
	x=f2.read()
	f1.close()
	print('***************************************************************************************************************************')
	#print(x)
	soup = BeautifulSoup(x,features="lxml")
	f2.close()
	for link in soup.select('div.kCrYT > a'):
		print("inside soup----->")
		print(link)
		linkReq= link.get("href")
		print("~~~~~~~~~~~~~~~LINK~~~~~~~~~~~~~~~~~~")
		print(linkReq)
		break

			
	MedicalSiteLink=linkReq.replace("/url?q=","")
	print(MedicalSiteLink)
	singlelink2=''
	if("&" in MedicalSiteLink):
				head, sep, tail = MedicalSiteLink.partition('&')
				print(head)
				singlelink2=head			
				res=requests.get(singlelink2, allow_redirects=True)
				p=res.content
				f5=open("page5.html","w")
				f5.write(str(p))
				f6=open("page5.html","r")
				x=f6.read()
				f5.close()


				soup = BeautifulSoup(x,features="lxml")
				f6.close()
				print("______________________________________________________________________________")
				for data in soup.select("div.review-wrapper"):
					#print(data.text)
					for k in data.select("p"):
						#print(k)
						flag=0
						Reviewtext=k.text.replace("\\xc2\\xa0","")
						t=Reviewtext.split()
						print(t)
						print("______________________________________________________________________________")
						for item in t:
							if (item=='\\n'):
								flag=1
								break
						if(flag==1):
							continue
						else:
							ListReviews.append(Reviewtext)
							MEDID.append(ID)



print("^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^")
print(ListReviews)
df0 = pd.DataFrame({'MEdID':MEDID,'Review':ListReviews})
print (df0)
df0.to_csv(csv_file)