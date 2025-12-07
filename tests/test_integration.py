import os
import pytest
from pprint import pprint
from dotenv import load_dotenv
from googleapiclient.discovery import build
from src.api_client import get_comment_threads


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
    assert "published" in first
    assert "likeCount" in first

    assert isinstance(first["author"], str)
    assert isinstance(first["text"], str)
    assert isinstance(first["published"], str)
    assert isinstance(first["likeCount"], int)

    pprint(comments)
    #pprint formats complex python objects so they are easy to read

    