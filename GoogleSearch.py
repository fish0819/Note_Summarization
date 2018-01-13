from google import search
import urllib
from bs4 import BeautifulSoup

NUM_PAGE = 3
query = 'data mining'
for url in search(query, stop = 10):
	thisPage = urllib.urlopen(url)
	soup = BeautifulSoup(thisPage, 'html.parser')
	print (soup.title.text)
	print (url)
# Results = google.search('python google search', NUM_PAGE)
# for result in Results:
# 	print (result.description)