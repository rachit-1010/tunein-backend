from flask import Flask, jsonify, request
import requests as pyrequests
from dotenv import load_dotenv
from pymongo import MongoClient
from bson import json_util
import os
import datetime
import uuid
from flask_cors import CORS
import jwt
from google.oauth2 import id_token
from google.auth.transport import requests


load_dotenv()

MONGODB_URI = os.getenv('MONGODB_URI')
YT_KEY = os.getenv('YT_KEY')
CLIENT_ID = os.getenv('CLIENT_ID')
JWT_SECRET = os.getenv('JWT_SECRET')

sample_search_result = {
		"kind": "youtube#searchListResponse",
		"etag": "uNcBn0F9U8m_bcwnVoCR21c54KY",
		"nextPageToken": "CAYQAA",
		"regionCode": "US",
		"pageInfo": {
			"totalResults": 1000000,
			"resultsPerPage": 6
		},
		"items": [
			{
			"kind": "youtube#searchResult",
			"etag": "LD990IjfgvN3kFXynQ2cb5plNM8",
			"id": {
				"kind": "youtube#video",
				"videoId": "YxWlaYCA8MU"
			},
			"snippet": {
				"publishedAt": "2022-12-22T05:30:09Z",
				"channelId": "UCbTLwN10NoCU4WDzLf1JMOA",
				"title": "Jhoome Jo Pathaan Song | Shah Rukh Khan, Deepika | Vishal &amp; Sheykhar, Arijit Singh, Sukriti, Kumaar",
				"description": "Can't stop ourselves from vibing to this absolute banger! #jhoomejopathaan ▻ Subscribe Now: https://goo.gl/xs3mrY Stay ...",
				"thumbnails": {
				"default": {
					"url": "https://i.ytimg.com/vi/YxWlaYCA8MU/default.jpg",
					"width": 120,
					"height": 90
				},
				"medium": {
					"url": "https://i.ytimg.com/vi/YxWlaYCA8MU/mqdefault.jpg",
					"width": 320,
					"height": 180
				},
				"high": {
					"url": "https://i.ytimg.com/vi/YxWlaYCA8MU/hqdefault.jpg",
					"width": 480,
					"height": 360
				}
				},
				"channelTitle": "YRF",
				"liveBroadcastContent": "none",
				"publishTime": "2022-12-22T05:30:09Z"
			}
			},
			{
			"kind": "youtube#searchResult",
			"etag": "ToonUSSvHlVPTZwMsruqO_3qFSU",
			"id": {
				"kind": "youtube#video",
				"videoId": "vqu4z34wENw"
			},
			"snippet": {
				"publishedAt": "2023-01-10T05:30:08Z",
				"channelId": "UCbTLwN10NoCU4WDzLf1JMOA",
				"title": "Pathaan Trailer | Shah Rukh Khan | Deepika Padukone | John Abraham | Siddharth A | YRF Spy Universe",
				"description": "Party Pathaan Ke Ghar Pe Rakhoge, Toh Mehmaan Nawaazi Ke Liye Pathaan Toh Aayega Aur, Pataakhe Bhi Laayega ...",
				"thumbnails": {
				"default": {
					"url": "https://i.ytimg.com/vi/vqu4z34wENw/default.jpg",
					"width": 120,
					"height": 90
				},
				"medium": {
					"url": "https://i.ytimg.com/vi/vqu4z34wENw/mqdefault.jpg",
					"width": 320,
					"height": 180
				},
				"high": {
					"url": "https://i.ytimg.com/vi/vqu4z34wENw/hqdefault.jpg",
					"width": 480,
					"height": 360
				}
				},
				"channelTitle": "YRF",
				"liveBroadcastContent": "none",
				"publishTime": "2023-01-10T05:30:08Z"
			}
			},
			{
			"kind": "youtube#searchResult",
			"etag": "_hsqWazH6Nt6z0ikp63-rJRqqas",
			"id": {
				"kind": "youtube#video",
				"videoId": "4xl9KfUg8Lc"
			},
			"snippet": {
				"publishedAt": "2022-11-02T05:31:19Z",
				"channelId": "UCbTLwN10NoCU4WDzLf1JMOA",
				"title": "Pathaan | Official Teaser | Shah Rukh Khan | Deepika Padukone | John Abraham | Siddharth Anand",
				"description": "Apni Kursi Ki Peti Baandh Lo… Mausam Bigadne Wala Hai #PathaanTeaser. ▻ Subscribe Now: https://goo.gl/xs3mrY Stay ...",
				"thumbnails": {
				"default": {
					"url": "https://i.ytimg.com/vi/4xl9KfUg8Lc/default.jpg",
					"width": 120,
					"height": 90
				},
				"medium": {
					"url": "https://i.ytimg.com/vi/4xl9KfUg8Lc/mqdefault.jpg",
					"width": 320,
					"height": 180
				},
				"high": {
					"url": "https://i.ytimg.com/vi/4xl9KfUg8Lc/hqdefault.jpg",
					"width": 480,
					"height": 360
				}
				},
				"channelTitle": "YRF",
				"liveBroadcastContent": "none",
				"publishTime": "2022-11-02T05:31:19Z"
			}
			},
			{
			"kind": "youtube#searchResult",
			"etag": "dSABITnlp3bB7iqAh1v63zrG924",
			"id": {
				"kind": "youtube#video",
				"videoId": "Ymu9wVN7pWs"
			},
			"snippet": {
				"publishedAt": "2022-03-02T06:03:23Z",
				"channelId": "UCbTLwN10NoCU4WDzLf1JMOA",
				"title": "Pathaan | Date Announcement | Shah Rukh Khan | Deepika Padukone | John Abraham",
				"description": "Make. Some. Noise! PATHAAN is here. Watch the date announcement video! ▻ Subscribe Now: https://goo.gl/xs3mrY Stay ...",
				"thumbnails": {
				"default": {
					"url": "https://i.ytimg.com/vi/Ymu9wVN7pWs/default.jpg",
					"width": 120,
					"height": 90
				},
				"medium": {
					"url": "https://i.ytimg.com/vi/Ymu9wVN7pWs/mqdefault.jpg",
					"width": 320,
					"height": 180
				},
				"high": {
					"url": "https://i.ytimg.com/vi/Ymu9wVN7pWs/hqdefault.jpg",
					"width": 480,
					"height": 360
				}
				},
				"channelTitle": "YRF",
				"liveBroadcastContent": "none",
				"publishTime": "2022-03-02T06:03:23Z"
			}
			},
			{
			"kind": "youtube#searchResult",
			"etag": "GJsbJqGXf27uB3_bjHJ71HfZmJs",
			"id": {
				"kind": "youtube#video",
				"videoId": "T_rupRQOJZM"
			},
			"snippet": {
				"publishedAt": "2022-12-22T05:57:31Z",
				"channelId": "UCaqouA5CPzxoMUTvz0OGe6A",
				"title": "Pathaan’s Theme",
				"description": "Provided to YouTube by yrfmusic Pathaan's Theme · Vocals PATHAAN ℗ Yash Raj Films Pvt. Ltd. Released on: 2022-12-22 ...",
				"thumbnails": {
				"default": {
					"url": "https://i.ytimg.com/vi/T_rupRQOJZM/default.jpg",
					"width": 120,
					"height": 90
				},
				"medium": {
					"url": "https://i.ytimg.com/vi/T_rupRQOJZM/mqdefault.jpg",
					"width": 320,
					"height": 180
				},
				"high": {
					"url": "https://i.ytimg.com/vi/T_rupRQOJZM/hqdefault.jpg",
					"width": 480,
					"height": 360
				}
				},
				"channelTitle": "Various Artists - Topic",
				"liveBroadcastContent": "none",
				"publishTime": "2022-12-22T05:57:31Z"
			}
			},
			{
			"kind": "youtube#searchResult",
			"etag": "jjPe5qWb_Eplef8yRH1Bq9fEJjs",
			"id": {
				"kind": "youtube#video",
				"videoId": "sM9Uqtia-Lo"
			},
			"snippet": {
				"publishedAt": "2023-06-28T10:31:06Z",
				"channelId": "UCbTLwN10NoCU4WDzLf1JMOA",
				"title": "Pathaan&#39;s Theme | Shah Rukh Khan | Sanchit, Ankit | Kit Bee | Magdalena Supel | YRF Spy Universe",
				"description": "Shining so bright, he's the knight! Feel the adrenaline rush with the 'Pathaan' theme. ▻ Subscribe Now: https://goo.gl/xs3mrY ...",
				"thumbnails": {
				"default": {
					"url": "https://i.ytimg.com/vi/sM9Uqtia-Lo/default.jpg",
					"width": 120,
					"height": 90
				},
				"medium": {
					"url": "https://i.ytimg.com/vi/sM9Uqtia-Lo/mqdefault.jpg",
					"width": 320,
					"height": 180
				},
				"high": {
					"url": "https://i.ytimg.com/vi/sM9Uqtia-Lo/hqdefault.jpg",
					"width": 480,
					"height": 360
				}
				},
				"channelTitle": "YRF",
				"liveBroadcastContent": "none",
				"publishTime": "2023-06-28T10:31:06Z"
			}
			}
		]
	}
	




client = MongoClient(MONGODB_URI)

app = Flask(__name__)
CORS(app)


'''
	The backend server is only to interact with the database
	Each user has its own database
		- Collection of saved songs for the user (contains all the info about the song and a unique ID for the user)
		- Collection of playlists for the user (contains the song IDs only) (it has the list of liked songs as well)
	
	There is a serarate database that contains all the songs that are saved by all the users (only admin has access)
	Also, there is a database to store the profile info of all user (only admin has access)
'''

def create_access_token(sub, name):
	payload = {
		'sub': sub,
		'name': name,
		'exp': datetime.datetime.utcnow() + datetime.timedelta(hours=1),
		'type': 'access'
	}
	return jwt.encode(payload, JWT_SECRET, algorithm='HS256')

def create_refresh_token(sub, name):
	token_id = str(uuid.uuid4())
	expires = datetime.datetime.utcnow() + datetime.timedelta(days=30)
	payload = {
		'sub': sub,
		'name': name,
		'jti': token_id,
		'exp': expires,
		'type': 'refresh'
	}
	token = jwt.encode(payload, JWT_SECRET, algorithm='HS256')
	db = client.get_database('users')
	db.get_collection('refresh_tokens').insert_one({
		'jti': token_id,
		'sub': sub,
		'expires': expires,
		'revoked': False
	})
	return token

def authorization(user_details):
	if user_details == "guest":
		return client.get_database('guest')
	elif not user_details or user_details == "null":
		return False
	else:
		try:
			payload = jwt.decode(user_details, JWT_SECRET, algorithms=['HS256'])
			if payload.get('type') != 'access':
				return False
			return client.get_database(payload['sub'])
		except jwt.ExpiredSignatureError:
			return "expired"
		except (jwt.InvalidTokenError, Exception):
			return False



@app.route('/getallsongs')
def get_all_songs():
	user_details = request.headers.get('Authorization')
	db = authorization(user_details)
	if db == "expired":
		return jsonify({'error': 'token_expired'}), 401
	if db == False:
		return jsonify({'loggedIn': False}), 401

	collection = db.get_collection('songs')

	# Sorted according to the date of insertion
	songs = list(collection.find().sort('_id', 1))
	
	json_songs = json_util.dumps(songs)

	return jsonify(json_songs), 200

@app.route('/getallplaylists')
def get_all_playlists():
	user_details = request.headers.get('Authorization')
	db = authorization(user_details)
	if db == "expired":
		return jsonify({'error': 'token_expired'}), 401
	if db == False:
		return jsonify({'loggedIn': False}), 401

	collection = db.get_collection('playlists')
	playlists = list(collection.find().sort('_id', 1))
	# Ensure Liked Songs is always first
	liked = [p for p in playlists if p.get('playlistName', '').startswith('Liked Songs')]
	others = [p for p in playlists if not p.get('playlistName', '').startswith('Liked Songs')]
	playlists = liked + others
	json_playlists = json_util.dumps(playlists)

	return jsonify(json_playlists), 200

@app.route('/getlogininfo')
def get_login_info():
	user_details = request.headers.get('Authorization')
	if user_details == "guest":
		return jsonify({"username": "guest"})
	if not user_details or user_details == "null":
		return jsonify({'loggedIn': False}), 401

	try:
		google_user = id_token.verify_oauth2_token(user_details, requests.Request(), CLIENT_ID)
	except Exception:
		return jsonify({'loggedIn': False, 'error': 'invalid_google_token'}), 401

	# check if user exists in the database
	db = client.get_database('users')
	collection = db.get_collection('users')
	# if user does not exist, add the user to the database
	if collection.find_one({'sub': google_user["sub"]}) is None:
		print("###################")
		print("NAYA BAKRA MILA")
		print("###################")
		collection.insert_one({'sub': google_user["sub"], 'email': google_user["email"], 'name': google_user["given_name"]})
		# also create a new database for the user
		user_db = client.get_database(google_user["sub"])
		songs_col = user_db.get_collection('songs')
		# copy all the songs from the guest database to the user's database
		source_db = client.get_database('guest')
		source_collection = source_db.get_collection('songs')
		documents_to_copy = list(source_collection.find())
		if documents_to_copy:
			songs_col.insert_many(documents_to_copy)
		# also create the first empty playlist - Liked Songs
		playlist_col = user_db.get_collection('playlists')
		playlist_col.insert_one({'playlistName': 'Liked Songs💚', 'songs': [], 'numSongs':0, 'totalDuration':'0 min'})

	# Issue custom JWT tokens
	access_token = create_access_token(google_user["sub"], google_user["given_name"])
	refresh_token = create_refresh_token(google_user["sub"], google_user["given_name"])

	return jsonify({
		"username": google_user["given_name"],
		"accessToken": access_token,
		"refreshToken": refresh_token
	})

@app.route('/createPlaylist', methods=['POST'])
def create_playlist():
	user_details = request.headers.get('Authorization')
	db = authorization(user_details)
	if db == "expired":
		return jsonify({'error': 'token_expired'}), 401
	if db == False:
		return jsonify({'loggedIn': False}), 401

	collection = db.get_collection('playlists')

	# get the POST request data
	data = request.get_json()
	playlist_name = data['playlistName']

	collection.insert_one({'playlistName': playlist_name, 'songs': [], 'numSongs':0, 'totalDuration':'0 min'})

	return jsonify({'success': True}), 200


@app.route('/addSongToPlaylist', methods=['POST'])
def add_song_to_playlist():
	user_details = request.headers.get('Authorization')
	db = authorization(user_details)
	if db == "expired":
		return jsonify({'error': 'token_expired'}), 401
	if db == False:
		return jsonify({'loggedIn': False}), 401

	collection = db.get_collection('playlists')

	# get the POST request data
	data = request.get_json()
	playlist_name = data['playlistName']
	songIndex = data['songIndex']
	print(playlist_name, songIndex)

	# get the playlist document
	playlist = collection.find_one({'playlistName': playlist_name})
	# add the songIndex to the songs array, increment the numSongs and update the totalDuration
	songs = playlist['songs']
	songs.append(songIndex)
	numSongs = playlist['numSongs']+1
	collection.update_one({'playlistName': playlist_name}, {'$set': {'songs': songs, 'numSongs': numSongs}})
	return jsonify({'success': True}), 200

@app.route('/removeSongFromPlaylist', methods=['POST'])
def remove_song_from_playlist():
	user_details = request.headers.get('Authorization')
	db = authorization(user_details)
	if db == "expired":
		return jsonify({'error': 'token_expired'}), 401
	if db == False:
		return jsonify({'loggedIn': False}), 401

	collection = db.get_collection('playlists')

	# get the POST request data
	data = request.get_json()
	playlist_name = data['playlistName']
	songIndex = data['songIndex']

	# get the playlist document
	playlist = collection.find_one({'playlistName': playlist_name})
	# remove the songIndex from the songs array, decrement the numSongs and update the totalDuration
	songs = playlist['songs']
	songs.remove(songIndex)
	numSongs = playlist['numSongs']-1
	collection.update_one({'playlistName': playlist_name}, {'$set': {'songs': songs, 'numSongs': numSongs}})
	return jsonify({'success': True}), 200

@app.route('/searchSongYT', methods=['POST'])
def search_song_yt():
	# get the POST request data
	data = request.get_json()
	search_query = data['searchQuery']
	print(search_query)

	params = {"key": YT_KEY, "q": search_query, "part": 'snippet', "maxResults": 6}
	r = pyrequests.get("https://www.googleapis.com/youtube/v3/search", params=params)
	result = r.json()
	return jsonify(result), 200
	# return jsonify(sample_search_result), 200

@app.route('/addSong', methods=['POST'])
def add_song():
	user_details = request.headers.get('Authorization')
	db = authorization(user_details)
	if db == "expired":
		return jsonify({'error': 'token_expired'}), 401
	if db == False:
		return jsonify({'loggedIn': False}), 401

	collection = db.get_collection('songs')

	# get the POST request data
	data = request.get_json()

	collection.insert_one({'title': data['title'], 'album': data['album'], 'duration': data['duration'], 'videoId': data['videoId']})

	return jsonify({'success': True}), 200

@app.route('/refresh', methods=['POST'])
def refresh():
	data = request.get_json()
	refresh_token = data.get('refreshToken')
	if not refresh_token:
		return jsonify({'error': 'missing_token'}), 400

	try:
		payload = jwt.decode(refresh_token, JWT_SECRET, algorithms=['HS256'])
	except jwt.ExpiredSignatureError:
		return jsonify({'error': 'refresh_expired'}), 401
	except jwt.InvalidTokenError:
		return jsonify({'error': 'invalid_token'}), 401

	if payload.get('type') != 'refresh':
		return jsonify({'error': 'wrong_token_type'}), 401

	db = client.get_database('users')
	stored = db.get_collection('refresh_tokens').find_one({
		'jti': payload['jti'], 'revoked': False
	})
	if not stored:
		return jsonify({'error': 'revoked_or_unknown'}), 401

	new_access = create_access_token(payload['sub'], payload.get('name', ''))
	return jsonify({'accessToken': new_access})

@app.route('/logout', methods=['POST'])
def logout_endpoint():
	data = request.get_json()
	refresh_token = data.get('refreshToken')
	if refresh_token:
		try:
			payload = jwt.decode(refresh_token, JWT_SECRET, algorithms=['HS256'], options={"verify_exp": False})
			db = client.get_database('users')
			db.get_collection('refresh_tokens').update_one(
				{'jti': payload.get('jti')},
				{'$set': {'revoked': True}}
			)
		except Exception:
			pass
	return jsonify({'success': True})

# Home Route
@app.route('/')
def home():
	return jsonify({'message': 'Welcome to the Music App Backend!'}), 200

if __name__ == '__main__':
	print(os.getenv('PORT'))
	app.run(debug=True, port=int(os.getenv('PORT', 5001)), host='0.0.0.0')
	