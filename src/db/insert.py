import psycopg2

from .connection import get_connection
from ..api_client import get_Channel_info

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
        print("Data inserted successfully!")
        
    except psycopg2.Error as e:
        print("Error Inserting: ", e)

    finally:
        cursor.close()
        conn.close()


   
    




      

              
        

    




