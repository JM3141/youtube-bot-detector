# importing os module for environment variables
import os

#From Google’s toolbox, take the build tool so I can create a doorway to YouTube’s data
from googleapiclient.discovery import build

# importing necessary functions from dotenv library
from dotenv import load_dotenv, dotenv_values
load_dotenv()

from datetime import datetime

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
            id = item["snippet"]["topLevelComment"]["id"]
            comment = item["snippet"]["topLevelComment"]
            author= comment["snippet"]["authorDisplayName"]
            text = comment["snippet"]["textOriginal"]
            publishedAt = comment["snippet"]["publishedAt"]
            likeCount = comment["snippet"]["likeCount"]
            author_channel_id = comment["snippet"]["authorChannelId"]["value"]
            author_profile_image_url = comment["snippet"]["authorProfileImageUrl"]
            author_channel_url = comment["snippet"]["authorChannelUrl"]
            updatedAt  = comment["snippet"]["updatedAt"]
     
            all_comments.append({
                "id": id,
                "author": author,
                "text": text,
                "publishedAt": parse_timestamp(publishedAt),
                "likeCount": likeCount,
                "authorChannelId": author_channel_id,
                "authorProfileImageUrl": author_profile_image_url,
                "authorChannelUrl": author_channel_url,
                "updatedAt": parse_timestamp(updatedAt)            
            })
        
    return all_comments



def parse_timestamp(ts: str) -> datetime:
    return datetime.fromisoformat(ts.replace("Z", "+00:00"))


def get_comment_list(youtube, parent_IDs):

    comments_replies = []

    for parent_ID in parent_IDs:
        results = youtube.comments().list(
        part = "snippet",
        parentId = parent_ID,
        maxResults = 5,
        textFormat = "plainText"
        ).execute()

        for item in results["items"]:
            id = item["id"]
            parent_id = item["snippet"]["parentId"]
            comment = item["snippet"]["textOriginal"]
            author_channel_id = item["snippet"]["authorChannelId"]["value"]
            author = item["snippet"]["authorDisplayName"]
            author_profile_image_url = item["snippet"]["authorProfileImageUrl"]
            author_channel_url = item["snippet"]["authorChannelUrl"]
            likeCount = item["snippet"]["likeCount"]
            publishedAt = item["snippet"]["publishedAt"]
            updatedAt  = item["snippet"]["updatedAt"]

            comments_replies.append({
                "id": id,
                "parentId": parent_id,
                "author": author,
                "text": comment,
                "publishedAt": parse_timestamp(publishedAt),
                "likeCount": likeCount,
                "authorChannelId": author_channel_id,
                "authorProfileImageUrl": author_profile_image_url,
                "authorChannelUrl": author_channel_url,
                "updatedAt": parse_timestamp(updatedAt)            
            })
     
    

    return comments_replies
    
   

#method to get all comments
def get_all_comments_for_videos(youtube, video_ids):
    result = {}

    for video_id in video_ids:
        top_comments = get_comment_threads(youtube, [video_id])

        for comment in top_comments:
            parent_id = comment["id"]
            replies = get_comment_list(youtube, [parent_id])
            comment["replies"] = replies

        result[video_id] = top_comments

    return result
    

def get_video_statistics(youtube, video_IDs):

    video_statistics = []

    for video_ID in video_IDs:
       results = youtube.videos().list(
       part = "statistics,snippet",
       id = video_ID
       ).execute()

       for item in results["items"]:
           id = item["id"]
           publishedAt = item["snippet"]["publishedAt"]
           viewCount = item["statistics"]["viewCount"]
           likeCount = item["statistics"]["likeCount"]
           commentCount = item["statistics"]["commentCount"]

           video_statistics.append({
                "id": id,
                "publishedAt": parse_timestamp(publishedAt),
                "viewCount": int(viewCount),
                "likeCount": int(likeCount),
                "commentCount": int(commentCount)
           })
               
    return video_statistics


def get_Channel_info(youtube, channel_IDs):

    channel_info = []

    for channel_ID in channel_IDs:
        results = youtube.channels().list(
        part = "id,snippet,statistics,contentDetails",
        id = channel_ID,
        maxResults = 5
        ).execute()

        for item in results["items"]:
            id = item["id"]
            title = item["snippet"]["title"]
            description  = item["snippet"]["description"]
            customUrl = item["snippet"]["customUrl"]
            publishedAt = item["snippet"]["publishedAt"]
            thumbnailUrl = item["snippet"]["thumbnails"]["high"]["url"]
            viewCount = item["statistics"]["viewCount"]
            subscriberCount = item["statistics"]["subscriberCount"]
            videoCount = item["statistics"]["videoCount"]
            uploads = item["contentDetails"]["relatedPlaylists"]["uploads"]

            channel_info.append({
                   "id": id,
                   "title": title,
                   "description": description,
                   "customUrl": customUrl,
                   "publishedAt": parse_timestamp(publishedAt),
                   "thumbnailUrl": thumbnailUrl,
                   "viewCount": int(viewCount),
                   "subscriberCount": int(subscriberCount),
                   "videoCount": int(videoCount),
                   "uploads": uploads
            })

    return channel_info




          






    

    
