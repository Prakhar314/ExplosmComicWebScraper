from bs4 import BeautifulSoup
import requests
from io import BytesIO
from PIL import Image
import os
def ensure(path):
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        os.makedirs(dir)
def useInput():
    f = open("input.txt",'r')
    inputData = [k.split() for k in f.readlines()]
    f.close()
    months = {'january':1,'february':2,'march':3,'april':4,'may':5,'june':6,'july':7,'august':8,'september':9,'october':10,'november':11,'december':12}
    for year in range(int(inputData[0][1]),int(inputData[1][1])+1):
        start = 1
        end = 12
        if year == int(inputData[0][1]):
            start = months[inputData[0][0]]
        elif year == int(inputData[1][1]):
            end = months[inputData[1][0]]
        for month in range(start,end+1):
            monthString = str(month)
            if month<10:
                monthString = "0"+monthString
            for key in months.keys():
                if months[key]==month:
                    break
            for author in inputData[2]:
                source = requests.get('http://explosm.net/comics/archive/'+str(year)+"/"+monthString+"/"+author.lower()).text
                soupS = BeautifulSoup(source,'lxml')
                cont = soupS.find('div', class_="small-7 medium-8 large-8 columns").find_all('div', class_="small-12 medium-12 large-12 columns")
                for containers in cont:
                    dateString = containers.find(id = "comic-author").text.split('<br>')[0].split()[0]
                    imgpage = requests.get('http://explosm.net'+containers.a['href']).text
                    soupI = BeautifulSoup(imgpage,'lxml')
                    comicLink = 'http:'+soupI.find(id = "main-comic")['src'].split('?')[0]
                    image_name = str(year)+'/'+key.capitalize()+'/'+dateString+'-'+author.capitalize()+'.png'
                    ensure(image_name)
                    r = requests.get(comicLink)
                    i = Image.open(BytesIO(r.content))
                    i.save(image_name)

