from bs4 import BeautifulSoup
import requests
from io import BytesIO
from PIL import Image
import os

months = {'january':1,'february':2,'march':3,'april':4,'may':5,'june':6,'july':7,'august':8,'september':9,'october':10,'november':11,'december':12}

#Ensure required folder
def ensure(path):
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        os.makedirs(dir)

def saveImage(comicLink,image_name):
    ensure(image_name)
    r = requests.get(comicLink)
    i = Image.open(BytesIO(r.content))
    i.save(image_name)
    print(image_name)

def currentTime():
    source = requests.get('http://explosm.net/comics/archive/').text
    soupS = BeautifulSoup(source,'lxml')
    currentPanel = soupS.find("dd",class_="accordion-navigation")
    currentMonth = months[currentPanel.find("li",class_="active").a.text.lower()]
    currentYear = int(currentPanel.div["id"][5:])
    return currentMonth,currentYear

def getMonth(month):
    for key in months.keys():
        if months[key]==month:
            break
    return key

#Input Type 1
def useInput(inputData):
    currentMonth,currentYear = currentTime()
    if int(inputData[1][1])>currentYear:
        inputData[1][1]=str(currentYear)
        inputData[1][0]='december'
    if int(inputData[1][1])==currentYear:
        if months[inputData[1][0]]>currentMonth:
            inputData[1][0]=getMonth(currentMonth)
    if int(inputData[0][1])<2005:
        inputData[0][1]='2005'
        inputData[0][0]='january'
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
            key = getMonth(month)
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
                    saveImage(comicLink,image_name)

#Input (Bonus) Type 1
def useRandom():
    source = requests.get('http://explosm.net/rcg').text
    soupS = BeautifulSoup(source,'lxml')
    panels = soupS.find("div",class_="rcg-panels").find_all("img")
    n=1
    for images in panels:
        comicLink = images["src"]
        image_name = "random/frame"+str(n)+".png"
        saveImage(comicLink,image_name)
        n+=1

#Input (Bonus) Type 2
def useLatest(N):
    currentMonth,currentYear = currentTime()
    while N>0:
        monthString = str(currentMonth)
        if currentMonth<10:
            monthString = "0"+monthString
        source = requests.get('http://explosm.net/comics/archive/'+str(currentYear)+"/"+monthString).text
        soupS = BeautifulSoup(source,'lxml')
        cont = soupS.find('div', class_="small-7 medium-8 large-8 columns").find_all('div', class_="small-12 medium-12 large-12 columns")
        for containers in cont:
            dateString = containers.find(id = "comic-author").text.split('<br>')[0].split()
            author=dateString[2]
            dateString=dateString[0]
            imgpage = requests.get('http://explosm.net'+containers.a['href']).text
            soupI = BeautifulSoup(imgpage,'lxml')
            comicLink = 'http:'+soupI.find(id = "main-comic")['src'].split('?')[0]
            image_name = 'latest/'+dateString+'-'+author+'.png'
            saveImage(comicLink,image_name)
            N-=1
            if N==0:
                break
        if N!=0:
            currentMonth-=1
            if currentMonth==0:
                currentMonth=12
                currentYear-=1
                if currentYear==2004:
                    print("No more comics")
                    N=0

f = open("input.txt",'r')
inputData = [k.split() for k in f.readlines()]
f.close()

if inputData[0][0].lower()=="random":
    useRandom()
elif inputData[0][0].lower()=="latest":
    useLatest(int(inputData[0][1]))
else:
    useInput(inputData)