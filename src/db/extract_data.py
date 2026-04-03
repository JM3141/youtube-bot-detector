import psycopg2
from .connection import get_connection


def load_raw_comments():

    try:
        conn = get_connection()
        cursor = conn.cursor()

        # sql query combining 3 tables
        # result is a list of tuples

        cursor.execute("""
            SELECT a.authorname, c."text", c.youtubecomment_id,
                   c.publishedat, c.updatedat, v.youtubevideo_id
            FROM "comment" c
            JOIN author a ON c.authorchannel_id = a.authorchannel_id
            JOIN video v ON c.video_id = v.video_id;                   
            """)
        
        results = cursor.fetchall()

        #converting SQL tuples into dictionaries
        #better for ML pipelines
        
        columns = ["authorname", "text", "youtubecomment_id", 
                   "publishedat", "updatedat", "youtubevideo_id"]
        
        dict_rows = [dict(zip(columns, row)) for row in results]

        # zip(columns, row) pairs each column name with the matching value in the tuple.

        return dict_rows

        

    except psycopg2.Error as e:
        print("Error extracting: ", e)
    
    finally:
        cursor.close()
        conn.close()
