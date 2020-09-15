import requests
import json
import pandas as pd
import matplotlib.pyplot as plt
import xmltodict
from reportlab.lib.styles import LineStyle


def get_news(msg_text,num):
 url = "https://newsapi.org/v2/everything?q=COVID&from=2020-03-16&sortBy=publishedAt&apiKey=426e591a64e44124bb388e53ef227ff1&pageSize=100&page=1"
 

 response = requests.request("GET", url)
 data=response.text
 data=json.loads(data)
 l=""
 a=[]

 for i in data["articles"]:
        title=i["title"]
        description=i["description"]
        url=i["url"]
        newString="Latest News\n"+""""""+str(title)+"""
active_case: """+str(description)+"""
recovered: """+str(url)
        l=newString
        print(newString)
        

        
 return(l)



