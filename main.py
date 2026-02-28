import os

from src.db.insert import insert_channel
from src.db.insert import insert_video
from src.api_client import searchForVideos


from dotenv import load_dotenv
load_dotenv()

from googleapiclient.discovery import build

def main():

    list_of_keywords = ["crypto", "crypto news",
                    "crypto trading", "robux",
                    "robux free", "robux gift card codes",
                    "robux giveaway", "roblox", "roblox gameplay",
                    "roblox adopt me", "roblox trading"]
    

    #accessing value and storing it in variable
    API_KEY = os.getenv("GOOGLE_API_KEY")

    #creating youtube resource object
    #build function contains API name, API version and API key
    youtube = build('youtube','v3', developerKey=API_KEY)
    
    
    videos = searchForVideos(youtube, list_of_keywords) 
    
    insert_channel(youtube, videos)
    insert_video(youtube, videos)
    

   
if __name__ == "__main__":
    main()

