from datetime import datetime


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
    

def get_video_statistics(youtube, video_ID):

    video_statistics = []

    # for video_ID in video_IDs:
    # results = youtube.videos().list(

    results = youtube.videos().list(
    part = "statistics,snippet",
    id = video_ID
    ).execute()

    for item in results["items"]:   
           id = item["id"]
           publishedAt = item["snippet"]["publishedAt"]
           viewCount = item["statistics"]["viewCount"]
           likeCount = item["statistics"]["likeCount"]

           #attempting to obtain commentCount else return None
           #not all videos have  a commentCount.
           commentCount = item["statistics"].get("commentCount")

           video_statistics.append({
                "id": id,
                "publishedAt": parse_timestamp(publishedAt),
                "viewCount": int(viewCount),
                "likeCount": int(likeCount),
                "commentCount": int(commentCount) if commentCount is not None else None
           })
               
    return video_statistics


def get_Channel_info(youtube, channel_ID):

        channel_info = []

        results = youtube.channels().list(
        part = "id,snippet,statistics,contentDetails",
        id = channel_ID,
        maxResults = 1
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


def get_Channel_Activity(youtube, channel_IDs):

    channel_Activity_info = []

    for channel_ID in channel_IDs:
        results = youtube.activities().list(
        part = "snippet,contentDetails",
        channelId = channel_ID,
        maxResults = 5
        ).execute()

        for item in results["items"]:
            publishedAt = item["snippet"]["publishedAt"]
            channelId = item["snippet"]["channelId"]
            type = item["snippet"]["type"]

            upload = None
            like = None
            playlistAdd = None

            if type == "upload":
                upload = item["contentDetails"]["upload"]["videoId"]
            
            elif type == "like":
                like = item["contentDetails"]["like"]["resourceId"]["videoId"]
            
            elif type == "playListItem":
                playlistAdd = item["contentDetails"]["playlistItem"]["resourceId"]["videoId"]

            channel_Activity_info.append({
                   "channelId": channelId,
                   "publishedAt": parse_timestamp(publishedAt),
                   "type": type,
                   "upload": upload,
                   "like": like,
                   "playListAdd": playlistAdd                  
            })

    return channel_Activity_info



def searchForVideos(youtube, list_of_keywords):
    #print("searchForVideos CALLED")

    #print("Keywords received:", list_of_keywords) 
    #print("Keyword count:", len(list_of_keywords))

    videos = []

    for keyword in list_of_keywords:

        #print("Searching for:", keyword)

        results = youtube.search().list(
        part = "snippet",
        q = keyword,
        type ="video",
        maxResults = 1
        ).execute()

        for item in results["items"]:

            #skip if item does not contain videoId
            if "videoId" not in item["id"]:
                continue

            videoId = item["id"]["videoId"]
            channelId = item["snippet"]["channelId"]
            title = item["snippet"]["title"]
            publishedAt = item["snippet"]["publishedAt"]
            channelTitle = item["snippet"]["channelTitle"]

            videos.append({
               "keyword": keyword,
               "videoId": videoId,
               "channelId": channelId,
               "title": title,
               "publishedAt": parse_timestamp(publishedAt),
               "channelTitle": channelTitle
            })

    #print("Total videos found:", len(videos))

    return videos
            


















        

     



          






    

    
