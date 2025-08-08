import requests
import os
from dotenv import load_dotenv
from pymongo import MongoClient
from bson import json_util

load_dotenv()
MONGODB_URI = os.getenv('MONGODB_URI')
YT_KEY = os.getenv('YT_KEY')
CLIENT_ID = os.getenv('CLIENT_ID')


client = MongoClient(MONGODB_URI)


# params = {"key": YT_KEY, "q": "Jhoome Jo Pathaan", "part": 'snippet', "maxResults": 6}
# r = requests.get("https://www.googleapis.com/youtube/v3/search", params=params)
# print(r.json())

def addSong():
	db = "108839854552737985500"
	db = client.get_database(db)
	collection = db.get_collection("songs")
	data = {
		"title": "Bom Diggy Diggy",
		"album": "Sonu Ke Titu Ki Sweety",
		"duration": "3:59",
		"videoId": "cgDe9D4BQTk"
	}
	collection.insert_one(data)

def getPlaylistSongs():
	db = "108839854552737985500"
	db = client.get_database(db)
	collection = db.get_collection("playlists")
	data = collection.find({"playlistName": "A.R. Rahman"})
	print(data[0]['songs'])
	
	# get all songs of user
	collection_songs = db.get_collection("songs")
	all_songs = list(collection_songs.find().sort('_id', 1))
	# print(all_songs[0])
	# filter out the songs at indexs given in data[0]['songs']
	songs_filter = []
	for index in data[0]['songs']:
		songs_filter.append(all_songs[index])
	print(songs_filter[-1])

	db_sravani = "105017686345308957298"
	db_sravani = client.get_database(db_sravani)
	collection_sravani = db_sravani.get_collection("songs")
	# add the filtered songs to the user's collection
	for song in songs_filter:
		collection_sravani.insert_one({"title": song["title"], "album": song["album"], "duration": song["duration"], "videoId": song["videoId"]})

def getallsongs():
	db_sravani = "105017686345308957298"
	db_sravani = client.get_database(db_sravani)
	collection_sravani = db_sravani.get_collection("songs")

	maha_songs = list(collection_sravani.find().sort('_id', 1))
	for i in range(len(maha_songs)):
		print(i, maha_songs[i]["title"])
	
	# plsongs = []
	# for i in range(230, 285):
	# 	plsongs.append(i)

	# collection_sravani.insert_one({"playlistName": "A.R. Rahman", "songs": plsongs, "numSongs": len(plsongs), "duration": "0 min"})

if __name__ == "__main__":
	addSong()
	# getPlaylistSongs()
	# getallsongs()