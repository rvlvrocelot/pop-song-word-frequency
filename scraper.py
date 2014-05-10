import requests
from bs4 import BeautifulSoup
import string
from HTMLParser import HTMLParser

class HTMLLyricParser(HTMLParser):
	lyrics = []

	def handle_comment(self, data):
		# Ignore comments
		pass

	def handle_data(self, data):
		# encode in unicode and tokenize
		self.lyrics.extend(unicode(data, errors='ignore').split())


def processLyrics(songName, artistName):
	r = requests.get("http://www.azlyrics.com/lyrics/" + artistName + "/" + songName + ".html")
	soup = BeautifulSoup(r.text)
	parser = HTMLLyricParser()
	lyrics =  str(soup.body.findAll(style="margin-left:10px;margin-right:10px;")[0])
	parser.feed(lyrics)
	print parser.lyrics

if __name__ == '__main__':
	processLyrics("letitgo", "idinamenzel")
