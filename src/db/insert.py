import psycopg2

from .connection import get_connection
from ..api_client import get_Channel_info
from ..api_client import get_video_statistics

def insert_channel(youtube, videos):
     
    try:
        conn = get_connection()
        cursor = conn.cursor()

        for video in videos:

           channel_info = get_Channel_info(youtube, video["channelId"])
       
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
            result = cursor.fetchone()[0]

            if not result:
                print(f"No channel found for {video["channelId"]}")
                continue

            insert_channel_id = result 

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



   
    




      

              
        

    




