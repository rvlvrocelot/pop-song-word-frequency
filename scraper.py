import requests
from bs4 import BeautifulSoup
import string
import HTMLParser

def processLyrics(songName, artistName):
	r = requests.get("http://www.azlyrics.com/lyrics/" + artistName + "/" + songName + ".html")
	data = r.text
	soup = BeautifulSoup(data)
	lyrics =  str(soup.body.findAll(style="margin-left:10px;margin-right:10px;")[0])
	splitLyrics = lyrics.split()
	splitLyrics = splitLyrics[splitLyrics.index('-->') + 1:]
	splitLyrics = splitLyrics[:splitLyrics.index('<!--')]
	print splitLyrics
	
processLyrics("letitgo","idinamenzel")
