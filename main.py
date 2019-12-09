from bs4 import BeautifulSoup
import requests
from io import BytesIO
from PIL import Image

source = requests.get('http://explosm.net/comics/archive').text
soupS = BeautifulSoup(source,'lxml')
cont = soupS.find('div', class_="small-7 medium-8 large-8 columns").find('div', class_="small-12 medium-12 large-12 columns")
imgpage = requests.get('http://explosm.net'+cont.a['href']).text
soupI = BeautifulSoup(imgpage,'lxml')
comicLink = 'http:'+soupI.find(id = "main-comic")['src'].split('?')[0]
image_name = 'test.png'
r = requests.get(comicLink)
i = Image.open(BytesIO(r.content))
i.save(image_name)