import requests
import os
from dotenv import load_dotenv

load_dotenv()
MONGODB_URI = os.getenv('MONGODB_URI')
YT_KEY = os.getenv('YT_KEY')
print(YT_KEY)
CLIENT_ID = os.getenv('CLIENT_ID')


params = {"key": YT_KEY, "q": "Jhoome Jo Pathaan", "part": 'snippet', "maxResults": 6}
r = requests.get("https://www.googleapis.com/youtube/v3/search", params=params)
print(r.json())
