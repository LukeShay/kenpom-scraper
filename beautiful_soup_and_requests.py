import requests
from bs4 import *

request = requests.get("https://www.google.com")

# print(request.status_code)
# print(request.headers)

src = request.content

soup = BeautifulSoup(src, 'lxml')

links = soup.find_all("a")

for link in links:
  if "About" in link.text:
    print(link)
    print(link.attrs['text'])
