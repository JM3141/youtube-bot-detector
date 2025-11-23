from unittest.mock import MagicMock
from src.api_client import get_comment_threads


def test_get_comment_threads():

    youtube = MagicMock()

    youtube.commentThreads().list().execute.return_value = {
      "items": [
          {  
               "snippet": {
                   "topLevelComment": {
                       "snippet": {
                           "authorDisplayName": "Test Author",
                           "textDisplay": "This is a fake comment",
                           "publishedAt": "2025-11-22T19:00:00Z",
                           "likeCount": 42
                       }
                    }

               }
              
          }

      ]
      
    }

    video_ids = ["fake_video1","fake_video2"]

    comments = get_comment_threads(youtube, video_ids)

    assert len(comments) == 2
    assert comments[0]["author"] == "Test Author"
    assert comments[0]["text"] == "This is a fake comment"
    assert comments[0]["published"] == "2025-11-22T19:00:00Z"
    assert comments[0]["likeCount"] == 42

