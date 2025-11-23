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

list_of_video_IDs =  ['jMrNjN0-osw', 'QKYFfYLe5rs', '3MfD_V0o_4U', 'yd_uG3TtREs', '5VYsnngkS_U', 'p2POGKxC0G8', 'gBuecIOZLV4', 'BKOVzHcjEIo', 'cfPHxW47E60', 'IEYDqdl9KbQ']

def get_comment_threads(youtube, video_IDs):

    all_comments = []

    for video_ID in video_IDs:
        results = youtube.commentThreads().list(
        part = "snippet",
        maxResults = 5,
        videoId = video_ID,
        textFormat = "plainText"
        ).execute()

        for item in results["items"]:
            comment = item["snippet"]["topLevelComment"]
            author= comment["snippet"]["authorDisplayName"]
            text = comment["snippet"]["textDisplay"]
            published = comment["snippet"]["publishedAt"]
            likeCount = comment["snippet"]["likeCount"]
            

            all_comments.append({
                "author": author,
                "text": text,
                "published": published,
                "likeCount": likeCount
            })
        
    return all_comments
    

    

