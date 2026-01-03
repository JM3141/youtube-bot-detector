import os
import pytest
from pprint import pprint
from dotenv import load_dotenv
from googleapiclient.discovery import build
from src.api_client import get_comment_threads
from src.api_client import get_all_comments_for_videos
from src.api_client import get_video_statistics
from datetime import datetime

#change this by adding the new attributes

load_dotenv()
API_KEY = os.getenv("GOOGLE_API_KEY")


@pytest.mark.integration
def test_get_comment_threads_real():

    if not API_KEY:
        pytest.skip("GOOGLE_API_KEY is not set in environment")

    #Create a real Youtube Client
    youtube = build('youtube','v3', developerKey=API_KEY)

    video_ids = ['jMrNjN0-osw']

    comments = get_comment_threads(youtube, video_ids)



    # Assertions: check structure, not exact text

    assert isinstance(comments, list)
    assert len(comments) > 0

    first = comments[0]
   
    assert "author" in first
    assert "text" in first
    assert "publishedAt" in first
    assert "likeCount" in first
    assert "authorChannelId" in first
    assert "authorProfileImageUrl" in first
    assert "authorChannelUrl" in first
    assert "updatedAt" in first

    assert isinstance(first["author"], str)
    assert isinstance(first["text"], str)
    assert isinstance(first["publishedAt"], datetime)
    assert isinstance(first["likeCount"], int)
    assert isinstance(first["authorChannelId"],str)
    assert isinstance(first["authorChannelUrl"],str)
    assert isinstance(first["updatedAt"],datetime)
    
    pprint(comments)
    #pprint formats complex python objects so they are easy to read

@pytest.mark.integration
def test_get_all_comments():

    if not API_KEY:
        pytest.skip("GOOGLE_API_KEY is not set in environment") 

    youtube = build('youtube', 'v3', developerKey=API_KEY)

    video_ids = ['AHRM_QNvp9E']

    comments = get_all_comments_for_videos(youtube, video_ids)

    assert isinstance(comments,dict)
    assert len(comments) > 0

    first = comments[video_ids[0]][0] 
    #first_replies = comments[video_ids[0]][0]["replies"]

    #assert len(first_replies) > 0

    assert "author" in first
    assert "text" in first
    assert "publishedAt" in first
    assert "likeCount" in first
    assert "authorChannelId" in first
    assert "authorProfileImageUrl" in first
    assert "authorChannelUrl" in first
    assert "updatedAt" in first

    assert isinstance(first["author"], str)
    assert isinstance(first["text"], str)
    assert isinstance(first["publishedAt"], datetime)
    assert isinstance(first["likeCount"], int)
    assert isinstance(first["authorChannelId"],str)
    assert isinstance(first["authorChannelUrl"],str)
    assert isinstance(first["updatedAt"],datetime)

    pprint(comments)

@pytest.mark.integration
def test_get_video_statistics_real():

    if not API_KEY:
        pytest.skip("GOOGLE_API_KEY is not set in environment") 

    youtube = build('youtube', 'v3', developerKey=API_KEY)

    video_ids = ['AHRM_QNvp9E']
    
    videos = get_video_statistics(youtube, video_ids)

    assert isinstance(videos, list)
    assert len(videos) > 0

    first = videos[0]

    assert "id" in first
    assert "publishedAt" in first
    assert "viewCount" in first
    assert "likeCount" in first
    assert "commentCount" in first

    assert isinstance(first["publishedAt"], datetime)
    assert isinstance(first["viewCount"], int)
    assert isinstance(first["likeCount"], int)
    assert isinstance(first["commentCount"], int)

    pprint(videos)



    





    