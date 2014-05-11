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
		html = top_100.html().encode('utf-8', errors='ignore')
		soup = BeautifulSoup(html)
		tr_all = soup.findAll('tr')
		for tr in tr_all:
			# filter by th - only those with scope=row and no class
			th_all = tr.findAll('th', {'scope': 'row', 'class': None})
			if len(th_all) == 0:
				continue

			td_all = tr.findAll('td')
			song = td_all[0].text.strip().replace('"', '')
			artist = td_all[1].text.strip().replace('"', '')
			song_list.add((artist, song))
			
	print song_list
	return song_list

if __name__ == '__main__':
	#process_lyrics("letitgo", "idinamenzel")
	year_list = [2000]
	song_list = get_top_100(year_list)
	print len(song_list)
