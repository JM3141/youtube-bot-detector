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









