import requests
from bs4 import *

KEN_POM_URL = 'https://kenpom.com/fanmatch.php?d=2019-04-06'

ken_pom_request = requests.get(KEN_POM_URL)

src = ken_pom_request.content

soup = BeautifulSoup(src, 'lxml')

links = soup.find_all('a')

for link in links:
  href = link.string + ""
  print(link.get('href'))
  print(href)
  temp = requests.get('https://kenpom.com/' + href)
  print(temp.content)
