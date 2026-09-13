import string


#Implementing simple numeric text features
#function takes 1 row at a time
def extract_text_features(row):

    text = row["text"]
    features = {}

    features["char_length"] = len(text)

    words = text.split()
    features["word_count"] = len(words)
     
    punctuation_count = sum (1 for ch in text if ch in string.punctuation)
    total_characters = len(text)
    features["punctuation_ratio"] = punctuation_count / total_characters

    uppercase_count = sum (1 for ch in text if ch in string.ascii_uppercase)
    features["uppercase_ratio"] = uppercase_count / total_characters

    #check if many repeated characters in string
    # 1 yes
    # 0 no

    previous = None
    run_length = 1
    repeated_flag = 0

    for ch in text:
        if ch == previous:
            run_length += 1
            if run_length >= 3:
                repeated_flag = 1
        else:
            run_length = 1
        previous = ch

    features["repeated_chars"] = repeated_flag

    #check if string has link
    
    has_link = 0

    if "http://" in text or "https://" in text or "www." in text:
        has_link = 1
    
    features["has_link"] = has_link

    return features

def extract_behavioural_features(all_rows):

    author_groups = {}
    video_groups = {}

    for row in all_rows:

        author = row["authorname"]
        video = row["youtubevideo_id"]

        #group rows by author name

        if author not in author_groups:
            author_groups[author] = []
            author_groups[author].append(row)
        
        #group rows by video
        if video not in video_groups:
            video_groups[video] = []
            video_groups[video].append(row)
        
    author_features = {}
   
    for author in author_groups:

        rows = author_groups[author]

        #number of comments made by author
        num_comments = len(rows)
        
        #number of unique videos
        unique_video_ids = set()

        for row in rows:
           unique_video_ids.add(row["youtubevideo_id"])
        
        num_of_unique_videos = len(unique_video_ids)
        
        #sorting list of comments by the time they were published
        rows.sort(key = lambda row: row["publishedat"])

        time_difference = []

        for i in range(1, len(rows)):
            current_time = rows[i]["publishedat"]
            previous_time = rows[i - 1]["publishedat"]
            diff = current_time - previous_time
            time_difference.append(diff)
        
        if len(time_difference) >= 1:
            average_time_between = sum(time_difference) / len(time_difference)
        else:
            average_time_between = None
        

        #examining comment behaviour, the predictability of the
        #waiting times between comments



        if len(time_difference) >= 2:

           mean = sum(time_difference) / len(time_difference)

           squared_distances = []

           for time in time_difference:
               distance_from_mean = time - mean
               squared_difference = distance_from_mean ** 2
               squared_distances.append(squared_difference)

           variance = sum(squared_distances)

           burstiness  = variance / mean

        else:
                 
           burstiness = None

        #checking if author posts the same text more than once.

        all_text = []  

        for row in rows:
            all_text.append(row["text"])

        text_counts = {}

        for text in all_text:

            if text in all_text:
                text_counts[text] += 1
            else:
                text_counts[text] = 1
        
        repeated_flag = 0
        for val in text_counts.values():
            if val >= 2:
                repeated_flag = 1
                break
        
        author_features[author] = {
            "author_num_comments": num_comments,
            "author_unique_videos": num_of_unique_videos,
            "author_avg_time_between": average_time_between,
            "author_burstiness": burstiness,
            "author_repeated_text": repeated_flag
        }
        

    #behavioural features per video

    video_features = {}

    for video in video_groups:

        rows = video_groups[video]

        #number of comments
        num_comments = len(rows)

        #number of unique authors
        unique_author_name = set()

        for row in rows:
            unique_author_name.add(row["authorname"])
        
        num_of_unique_authors = len(unique_author_name)
        
        
        #comment velocity(comments per hour)

        #sorting list of comments by the time they were published
        rows.sort(key = lambda row: row["publishedat"])

        
        if len(rows) >= 2:

            first_time = rows[0]["publishedat"]
            last_time = rows[-1]["publishedat"]

            #difference is a timedelta representing the time span.
            #difference.total_seconds() converts that span into seconds.
            #total_seconds  is a  float value that represents  duration in seconds
            #You divide by 3600 to get hours.


            difference = last_time - first_time
            total_seconds = difference.total_seconds()
            total_hours = total_seconds / 3600

            if total_hours > 0:

                comment_velocity = num_comments / total_hours

            else:

                comment_velocity = None
        
        else:
        
            comment_velocity = None
        
        
        video_features[video] = {
            "video_num_comments": num_comments,
            "video_unique_authors": unique_author_name,
            "video_comment_velocity": comment_velocity
        }

    return author_features, video_features


def extract_timing_features(row):
       
    timing_features = {}

    hour = row["publishedat"].hour

    dayOfWeek = row["publishedat"].weekday()

    isEdited = False

    if row["publishedat"] != row["updatedat"]:
        isEdited = True

    timing_features["hour_of_day"] = hour

    timing_features["day_of_week"] = dayOfWeek

    timing_features["was_edited"] = isEdited

    return  timing_features

    



    
    

    

    
       

       

       






























        







      





        

  
        









  
















