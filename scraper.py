import requests
from bs4 import BeautifulSoup
import string
from HTMLParser import HTMLParser
import wikipedia
import time
from collections import defaultdict

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
	time.sleep(2)
	r = requests.get("http://www.azlyrics.com/lyrics/" + artistName + "/" + songName + ".html")
	soup = BeautifulSoup(r.text)
	parser = HTMLLyricParser()
	lyrics =  str(soup.body.findAll(style="margin-left:10px;margin-right:10px;")[0])
	parser.feed(lyrics)
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
			if "(" in song: song = song[:song.find("(")]
			if "featuring" in song: song = song[:song.find("featuring")]
			song = ''.join(ch for ch in song if ch.isalnum())
			
			artist = td_all[1].text.strip().replace('"', '')
                        if "(" in artist: artist = artist[:artist.find("(")]
                        if "featuring" in artist: artist = artist[:artist.find("featuring")]
                        artist = ''.join(ch for ch in artist if ch.isalnum())
		
			song_list.add((artist, song, year))
			
	print song_list
	return song_list

def put_in_dict(song,artist,year,tempDict):
	#Jacob will definitely change this function name but whatever
	lyricsList = process_lyrics(song,artist)
	print song
	for word in lyricsList:
		if word == "love" : print word

	for word in lyricsList:
		if word not in tempDict[year]:
			tempDict[year][word] = 0
		tempDict[year][word] += 1
	print tempDict[2000]["love"]

def invert_dict(yearDict):
	newDict = defaultdict(dict)
	for year in yeardict:
		for word in yearDict[year]:
			newDict[word][year] = yearDict[year][word]
	print newDict 
		


if __name__ == '__main__':
	#process_lyrics("letitgo", "idinamenzel")
	year_list = [2000]
	song_list = get_top_100(year_list)
	#print len(song_list)
	tempDict = defaultdict(dict)
	for artist, song, year in song_list:
                song = song.lower().replace(' ', '')
                artist = artist.lower().replace(' ', '')
               # try:
                put_in_dict(song, artist,year,tempDict)
              #  except:
             #		print song,artist

	invert_dict(tempDict)
