import re
import requests
from bs4 import BeautifulSoup

site = 'https://www.ibeaschool.org/gallery'

response = requests.get(site)

soup = BeautifulSoup(response.text, 'html.parser')
img_tags = soup.find_all('img')

# we have to use 'data-src' because squarespace is an evil, evil pile of garbage
urls = [img['data-src'] for img in img_tags]


for url in urls:
    # we have to match \+ because these urls are fucking awful
    filename = re.search(r'/([\w\+_-]+[.](JPG|jpg|jpeg|gif|png))$', url)
    if not filename:
         print("Regex didn't match with the url: {}".format(url))
         continue
    with open(filename.group(1), 'wb') as f:
        if 'http' not in url:
            # sometimes an image source can be relative 
            # if it is provide the base url which also happens 
            # to be the site variable atm. 
            url = '{}{}'.format(site, url)
        response = requests.get(url)
        f.write(response.content)

