import psycopg2

from .connection import get_connection
from ..api_client import get_Channel_info
from ..api_client import get_video_statistics
from ..api_client import get_Channel_Activity
from ..api_client import get_all_comments_for_videos

def insert_channel(youtube, videos):
     
    try:
        conn = get_connection()
        cursor = conn.cursor()

        for video in videos:

           channel_info = get_Channel_info(youtube, video["channelId"])

           if not channel_info:
               print(f"No channel info for {video["channelId"]}")
               continue
       
           insert_query = """ 
                  INSERT INTO channel (youtubechannel_id, title, 
                                       description, customurl, publishedat,
                                       thumbnailurl, viewcount, subscribercount,
                                       videocount, uploads)
                  VAlUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                  ON CONFLICT (youtubechannel_id) DO NOTHING;
                  """
        
           data = (video["channelId"], channel_info[0]["title"], 
                channel_info[0]["description"], channel_info[0]["customUrl"],
                channel_info[0]["publishedAt"], channel_info[0]["thumbnailUrl"],
                channel_info[0]["viewCount"], channel_info[0]["subscriberCount"],
                channel_info[0]["videoCount"], channel_info[0]["uploads"])
          
           cursor.execute(insert_query, data)

           channel_activity = get_Channel_Activity(youtube, video["channelId"])

           if not channel_activity:
               print(f"No channel activity for {video["channelId"]}")
               continue
           
           cursor.execute("""
                 SELECT channel_id
                 FROM channel
                 WHERE youtubechannel_id = %s
             """, (video["channelId"],)
           ) 

           #extracting the int result from the tuple returned
           result = cursor.fetchone()

           if not result:
               print(f"No channel found for {video["channelId"]}")
            
           insert_channel_id = result[0]

           insert_activity = """
                 INSERT INTO channel_activity (youtubeactivity_id, publishedAt, 
                                               type, video_id_of_action, channel_id)
                 VALUES(%s, %s, %s, %s, %s)
                 ON CONFLICT (youtubeactivity_id) DO NOTHING;
                 """
           
           data2 = (channel_activity[0]["id"], channel_activity[0]["publishedAt"],
                    channel_activity[0]["type"], channel_activity[0]["video_id_of_action"],
                    insert_channel_id)
           
           cursor.execute(insert_activity, data2)
             
        conn.commit()
        print("Channel data inserted successfully!")
        
    except psycopg2.Error as e:
        print("Error Inserting: ", e)

    finally:
        cursor.close()
        conn.close()


def insert_video(youtube, videos):

    try:
        conn = get_connection()
        cursor = conn.cursor()

        for video in videos:

            video_stats = get_video_statistics(youtube, video["videoId"])

            if not video_stats:
                print(f"No stats returned for video {video["videoId"]}")
                continue
         
            cursor.execute("""
                 SELECT channel_id
                 FROM channel
                 WHERE youtubechannel_id = %s
             """, (video["channelId"],)
            )
           
            #extracting the int result from the tuple returned
            result = cursor.fetchone()

            if not result:
                print(f"No channel found for {video["channelId"]}")
                continue

            insert_channel_id = result[0] 

            #skipping if an insert tries to add a row with a youtubevideo_id that
            #already exists
  
            insert_query = """
                    INSERT INTO video (channel_id, viewcount, likecount, 
                                     commentcount, youtubevideo_id)
                    VALUES(%s, %s, %s, %s, %s)
                    ON CONFLICT (youtubevideo_id) DO NOTHING;
                    """
            
            data = (insert_channel_id, video_stats[0]["viewCount"], 
                    video_stats[0]["likeCount"], video_stats[0]["commentCount"],
                    video["videoId"])
            
            cursor.execute(insert_query, data)

        conn.commit()
        print("Video data inserted successfully!")
    
    except psycopg2.Error as e:
        print("Error Inserting ", e)
    
    finally:
        cursor.close()
        conn.close()


def get_author(youtube, videos):

    try:
        conn = get_connection()
        cursor = conn.cursor()
    
        for video in videos:

            all_comments  = get_all_comments_for_videos(youtube, video["videoId"])

            if not all_comments:
               print(f"No comments for this video {video["videoId"]}")

            comments = all_comments[video["videoId"]]

            insert_author_query = """
                INSERT INTO author (youtubechannel_id, authorname, 
                authorprofileimageurl, authorchannelurl)
                VALUES(%s, %s, %s, %s)
                ON CONFLICT (youtubechannel_id) DO NOTHING     
            """
            for comment in comments:

                if "authorChannelId" not in comment:
                    print("Skipping content with missing authorChannelId")
                    continue
        
                data = (comment["authorChannelId"], comment.get("author"), 
                    comment.get("authorProfileImageUrl"), comment.get("authorChannelUrl"))
        
                cursor.execute(insert_author_query, data)

                #process replies safely

                for reply in comment.get("replies", []):

                    if "authorChannelId" not in reply:
                        print("Skipping reply with missing authorChannelId")

                    data2 = (reply["authorChannelId"], reply["author"], 
                        reply["authorProfileImageUrl"], reply["authorChannelUrl"])
                
                    cursor.execute(insert_author_query, data2)
      
        conn.commit()
        print("Author has been inserted successfully")  

    except psycopg2.Error as e:
        print("Error inserting ", e)

    finally:
        cursor.close()
        conn.close() 




def get_comments(youtube, videos):

    try:
        conn = get_connection()
        cursor = conn.cursor()
    
        for video in videos:
            
            #fetch all comments for video
            all_comments  = get_all_comments_for_videos(youtube, video["videoId"])

            if not all_comments:
               print(f"No comments for this video {video["videoId"]}")

            comments = all_comments[video["videoId"]]

            #fetch DB video_id ONCE per video (foreign key)

            cursor.execute("""
                 SELECT video_id
                 FROM video
                 WHERE youtubevideo_id = %s
            """, (video["videoId"],)
            )

            video_row = cursor.fetchone()

            if not video_row:
                print(f"No video id found for video {video["videoId"]}")
                continue

            video_db_id = video_row[0]

            for comment in comments:

                if "id" not in comment or "text" not in comment:
                    print("Skipping malformed comment")
                    continue

                cursor.execute("""
                    SELECT authorchannel_id
                    FROM author
                    WHERE youtubechannel_id = %s
                """, (comment["authorChannelId"],)
                )

                row1 = cursor.fetchone()

                if not row1:
                    print("No author id found")
                    continue

                author_db_id = row1[0]
              

                #insert top level comment
                insert_comment_query = """
                    INSERT INTO comment (youtubecomment_id, text, 
                    publishedat, likecount, authorchannel_id, updatedat,
                    replycount, isreply, video_id)
                    VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (youtubecomment_id) DO NOTHING    
                """

                data = (comment["id"], comment["text"], 
                        comment["publishedAt"], comment["likeCount"],
                        author_db_id, comment["updatedAt"], comment["replyCount"], 
                        False, video_db_id)
    
                cursor.execute(insert_comment_query, data)

                for reply in comment.get("replies", []):

                    cursor.execute("""
                       SELECT authorchannel_id
                       FROM author
                       WHERE youtubechannel_id = %s
                    """,(reply["authorChannelId"],)                     
                    )

                    row2 = cursor.fetchone()
                    
                    if not row2:
                       print("No author channel id found for reply")
                       continue

                    reply_author_db_id = row2[0]
                   
                    insert_reply_query = """
                       INSERT INTO comment (youtubecomment_id, parent_id, text, 
                       publishedat, likecount, authorchannel_id, updatedat, isreply, video_id)
                       VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)
                       ON CONFLICT (youtubecomment_id) DO NOTHING    
                    """

                    data2 = (reply["id"], reply["parentId"], reply["text"], 
                      reply["publishedAt"], reply["likeCount"],
                      reply_author_db_id, reply["updatedAt"], 
                      False, video_db_id)
                    
                    cursor.execute(insert_reply_query, data2)

        conn.commit()
        print("Comments have been inserted successfully")

    except psycopg2.Error as e:
        print("Error inserting ", e)

    finally:
        cursor.close()
        conn.close() 











   
    




      

              
        

    




