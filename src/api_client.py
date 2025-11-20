# importing os module for environment variables
import os

#From Google’s toolbox, take the build tool so I can create a doorway to YouTube’s data
from googleapiclient.discovery import build

# importing necessary functions from dotenv library
from dotenv import load_dotenv, dotenv_values
load_dotenv()

#accessing value and storing it in variable
API_KEY = os.getenv("GOOGLE_API_KEY")

#creating youtube resource object
#build function contains API name, API version and API key
youtube = build('youtube','v3', developerKey=API_KEY)

video_ids =  ['jMrNjN0-osw', 'QKYFfYLe5rs', '3MfD_V0o_4U', 'yd_uG3TtREs', '5VYsnngkS_U', 'p2POGKxC0G8', 'gBuecIOZLV4', 'BKOVzHcjEIo', 'cfPHxW47E60', 'IEYDqdl9KbQ']

def get_comment_threads(youtube, video_ID):
    results = youtube.commentThreads().list(
    part = "snippet",
    maxResults = 1,
    videoId = video_ID,
    textFormat = "plainText"
    ).execute()

    for item in results["items"]:
        comment = item["snippet"]["topLevelComment"]
        author= comment["snippet"]["authorDisplayName"]
        text = comment["snippet"]["textDisplay"]
        published = comment["snippet"]["publishedAt"]
        likeCount = comment["snippet"]["likeCount"]
        print(author, text, published, likeCount)

    return results["items"]

get_comment_threads(youtube, video_ids[0])