import requests
from bs4 import BeautifulSoup
import string
from HTMLParser import HTMLParser
import wikipedia

class HTMLLyricParser(HTMLParser):
	lyrics = []

	def handle_comment(self, data):
		# Ignore comments
		pass

	def handle_data(self, data):
		# encode in unicode and tokenize
		self.lyrics.extend(unicode(data, errors='ignore').split())

# pep8:
# Function names should be lowercase, with words separated by underscores as necessary to improve readability.
def process_lyrics(songName, artistName):
	r = requests.get("http://www.azlyrics.com/lyrics/" + artistName + "/" + songName + ".html")
	soup = BeautifulSoup(r.text)
	parser = HTMLLyricParser()
	lyrics =  str(soup.body.findAll(style="margin-left:10px;margin-right:10px;")[0])
	parser.feed(lyrics)
	print parser.lyrics
	return parser.lyrics

def get_top_100(year_list):
	song_list = set()
	for year in year_list:
		top_100 = wikipedia.page('Billboard_Year-End_Hot_100_singles_of_{year}'.format(year=year))
		song_list.update([s for s in top_100.links if 'Billboard Year-End Hot 100 singles' not in s])

	print song_list
	return song_list

if __name__ == '__main__':
	process_lyrics("letitgo", "idinamenzel")
	year_list = ['2000', '2001']
	get_top_100(year_list)
