from unittest.mock import MagicMock
from src.api_client import get_comment_threads
from src.api_client import get_all_comments_for_videos
from src.api_client import get_video_statistics
from src.api_client import get_Channel_info
from src.api_client import parse_timestamp



def test_get_comment_threads():

    youtube = MagicMock()

    youtube.commentThreads().list().execute.return_value = {
      "items": [
          {             
               "snippet": {
                   "topLevelComment": {
                       "id": "COMMENT_ID_12345",  
                       "snippet": {                      
                           "authorDisplayName": "Test Author",
                           "textOriginal": "This is a fake comment",
                           "publishedAt": "2025-11-22T19:00:00Z",
                           "likeCount": 42,
                           "authorChannelId": { "value": "UC1234567890FAKEID" },
                           "authorProfileImageUrl": "https://example.com/avatar.png",
                           "authorChannelUrl": "https://www.youtube.com/channel/UC1234567890FAKEID",
                           "updatedAt": "2025-12-13T19:00:00Z"
                       }
                    }

               }
              
          }

      ]
      
    }

    video_ids = ["fake_video1","fake_video2"]

    comments = get_comment_threads(youtube, video_ids)

    assert len(comments) == 2
    assert comments[0]["id"] == "COMMENT_ID_12345"
    assert comments[0]["author"] == "Test Author"
    assert comments[0]["text"] == "This is a fake comment"
    assert comments[0]["publishedAt"] == parse_timestamp("2025-11-22T19:00:00Z")
    assert comments[0]["likeCount"] == 42
    assert comments[0]["authorChannelId"] =="UC1234567890FAKEID"
    assert comments[0]["authorProfileImageUrl"] == "https://example.com/avatar.png"
    assert comments[0]["authorChannelUrl"] == "https://www.youtube.com/channel/UC1234567890FAKEID"
    assert comments[0]["updatedAt"] == parse_timestamp("2025-12-13T19:00:00Z")

def test_get_all_comments():
    
    youtube = MagicMock()

    youtube.commentThreads.return_value.list.return_value.execute.return_value = {
      "items": [
          {             
               "snippet": {
                   "topLevelComment": {
                       "id": "COMMENT_ID_12345",  
                       "snippet": {                      
                           "authorDisplayName": "Test Author",
                           "textOriginal": "This is a fake comment",
                           "publishedAt": "2025-11-22T19:00:00Z",
                           "likeCount": 42,
                           "authorChannelId": { "value": "UC1234567890FAKEID" },
                           "authorProfileImageUrl": "https://example.com/avatar.png",
                           "authorChannelUrl": "https://www.youtube.com/channel/UC1234567890FAKEID",
                           "updatedAt": "2025-12-13T19:00:00Z"
                       }
                    }

               }
              
          }

      ]
      
    }  

    # mock replies
    youtube.comments.return_value.list.return_value.execute.return_value = {
        "items": [
            {                
                 "id": "REPLY_ID_007",
                 "snippet": {
                     "parentId": "COMMENT_ID_12345",
                     "authorDisplayName": "Reply Author",
                     "textOriginal": "This is a fake reply",
                     "publishedAt": "2025-12-01T10:00:00Z",
                     "likeCount": 5,
                     "authorChannelId": { "value": "UCFAKE_REPLY_CHANNEL_001" },
                     "authorProfileImageUrl": "https://example.com/reply-avatar.png",
                     "authorChannelUrl": "https://www.youtube.com/channel/UCFAKE_REPLY_CHANNEL_001",
                     "updatedAt": "2025-12-02T10:00:00Z"
                 }
            }
        ]
    }

    video_ids = ["fake_video1","fake_video2"]

    comments = get_all_comments_for_videos(youtube, video_ids)

    assert len(comments) == 2

    video1_comments = comments["fake_video1"]

    assert video1_comments[0]["id"] == "COMMENT_ID_12345"
    assert len(video1_comments[0]["replies"]) == 1
    assert video1_comments[0]["replies"][0]["id"] == "REPLY_ID_007"

def test_get_video_statistics():

    youtube = MagicMock()

    youtube.videos.return_value.list.return_value.execute.return_value = {
        "items": [
             {
                 "id": "abc123xyz",
                 "snippet": {
                     "publishedAt": "2023-05-14T12:30:00Z"
                  },
                  "statistics": {
                      "viewCount": 15432,
                      "likeCount": 842,
                      "commentCount": 129
                  }
                 
             }

         ]
    }

    video = ["fake_video1","fake_video2"]

    video_statistics = get_video_statistics(youtube, video)

    assert len(video_statistics) == 2

    assert video_statistics[0]["id"] == "abc123xyz"
    assert video_statistics[0]["publishedAt"] == parse_timestamp("2023-05-14T12:30:00Z")
    assert video_statistics[0]["viewCount"] == 15432
    assert video_statistics[0]["likeCount"] == 842
    assert video_statistics[0]["commentCount"] == 129


def test_get_Channel_info():

    youtube = MagicMock()

    youtube.channels.return_value.list.return_value.execute.return_value = {
        "items": [
            {
                "id": "abc345xyz",
                "snippet": {
                    "title": "TotalFootball Highlights",
                    "description": "Daily football highlights and tactical breakdowns.",
                    "customUrl": "https://www.youtube.com/@TotalFootballHighlights",
                    "publishedAt": "2023-05-14T12:30:00Z",
                    "thumbnails": {
                        "high": { 
                          "url": "https://yt3.ggpht.fakecdn.com/a/AATXAJzff001_high.jpg" 
                        }
                    }
                },

                "contentDetails": {
                   "relatedPlaylists": {                      
                        "uploads": "UUfakechanneluploads01"
                    }
                },

                "statistics": {
                    "viewCount": 15420392,
                    "subscriberCount": 482000,
                    "videoCount": 1264
                }

            }

        ]

    }

    channel = ["fakechannel1","fakechannel2"]

    channel_info = get_Channel_info(youtube, channel)
    
    assert len(channel) == 2

    assert channel_info[0]["id"] == "abc345xyz"
    assert channel_info[0]["title"] == "TotalFootball Highlights"
    assert channel_info[0]["description"] == "Daily football highlights and tactical breakdowns."
    assert channel_info[0]["customUrl"] == "https://www.youtube.com/@TotalFootballHighlights"
    assert channel_info[0]["publishedAt"] == parse_timestamp("2023-05-14T12:30:00Z") 
    assert channel_info[0]["thumbnailUrl"] == "https://yt3.ggpht.fakecdn.com/a/AATXAJzff001_high.jpg" 
    assert channel_info[0]["uploads"] == "UUfakechanneluploads01"
    assert channel_info[0]["viewCount"] == 15420392
    assert channel_info[0]["subscriberCount"] == 482000
    assert channel_info[0]["videoCount"] == 1264
