import requests
from bs4 import BeautifulSoup
import string
from HTMLParser import HTMLParser
import wikipedia
import time
from collections import defaultdict
import xml.etree.ElementTree as ET
import json

musixmatch_api_key = ''

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
	print parser.lyrics
	lyrics =  str(soup.body.findAll(style="margin-left:10px;margin-right:10px;")[0])
	parser.feed(lyrics)
	return parser.lyrics

def search_lyrics(artist, song):
	url = "http://api.chartlyrics.com/apiv1.asmx/SearchLyric?artist={artist}&song={song}".format(
		artist=artist, song=song
	)
	req = requests.get(url, timeout=10)
	tree = ET.fromstring(req.text)
	# only use first search result
	lyric_id_element = tree[0].find('{http://api.chartlyrics.com/}LyricId')
	if lyric_id_element is None:
		# didn't find anything
		return None, None
	lyric_check_sum_element = tree[0].find('{http://api.chartlyrics.com/}LyricChecksum') 
	return lyric_id_element.text, lyric_check_sum_element.text

def search_lyrics_musixmatch(artist, song):
	url = "http://api.musixmatch.com/ws/1.1/track.search?apikey={apikey}&q_artist={artist}&q_track={song}&format=json&page_size=1&f_has_lyrics=1".format(
		apikey=musixmatch_api_key, artist=artist, song=song
	)
	req = requests.get(url, timeout=10)
	response_json = json.loads(req.text)
	# only want first result
	first_track = response_json['message']['body']['track_list'][0]
	return first_track['track']['track_id']

def get_lyrics_musixmatch(track_id):
	url = "http://api.musixmatch.com/ws/1.1/track.lyrics.get?apikey={apikey}&track_id={track_id}&format=json".format(
		apikey=musixmatch_api_key, track_id=track_id
	)
	req = requests.get(url, timeout=10)
	response_json = json.loads(req.text)
	print response_json
	return response_json['message']['body']['lyrics']['lyrics_body']

def search_lyric_direct(artist, song):
	url = "http://api.chartlyrics.com/apiv1.asmx/SearchLyricDirect?artist={artist}&song={song}".format(
		artist=artist, song=song
	)
	req = requests.get(url, timeout=10)
	tree = ET.fromstring(req.text)
	# only use first search result
	lyric_element = tree.find('{http://api.chartlyrics.com/}Lyric')
	if lyric_element is None:
		return None
	else:
		return lyric_element.text


def get_lyrics_by_id(lyric_id, lyric_check_sum):
	url = "http://api.chartlyrics.com/apiv1.asmx/GetLyric?lyricId={lyricId}&lyricCheckSum={lyricCheckSum}".format(
		lyricId=lyric_id, lyricCheckSum=lyric_check_sum
	)
	print url
	req = requests.get(url, timeout=10)
	print req.text
	tree = ET.fromstring(req.text)
	lyric_element = tree.find('{http://api.chartlyrics.com/}Lyric')
	print lyric_element.text

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
			#if "(" in song: song = song[:song.find("(")]
			#if "featuring" in song: song = song[:song.find("featuring")]
			#print song
			#song = ''.join(ch for ch in song if ch.isalnum())
			#print song
			
			artist = td_all[1].text.strip().replace('"', '')
                        #if "(" in artist: artist = artist[:artist.find("(")]
                        #if "featuring" in artist: artist = artist[:artist.find("featuring")]
                        #artist = ''.join(ch for ch in artist if ch.isalnum())
		
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

def tree(): return defaultdict(tree)

def count_words_by_year(lyrics, year, word_count):
	lyrics_list = lyrics.split()
	for word in lyrics_list:
		if word not in word_count[year]:
			word_count[year][word] = 0
		word_count[year][word] += 1

		if year not in word_count[word]:
			word_count[word][year] = 0
		word_count[word][year] += 1
		
if __name__ == '__main__':
	year_list = [2000]
	song_list = get_top_100(year_list)
	word_count = tree()
	for artist, song, year in song_list:
		print artist, song, year
		try:
			lyrics = search_lyric_direct(artist, song)	
		except requests.exceptions.Timeout:
			print 'timeout'
			continue
		# don't hammer the API
		time.sleep(10)
		# didn't find anything for that arist/song
		print 'sleep over'
		if lyrics is None:
			print 'none found'
			continue

		count_words_by_year(lyrics, year, word_count)

	print word_count
