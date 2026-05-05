import pandas as pd

#loading the dataset
df = pd.read_csv("datasets/features.csv")

#rows on isBot column for current csv file is currently set to None for each comment

#decision to use iterrows() to modify each row in isBot column
# 1 indicates Bot comment
# 0 indicates Human comment

#creating manual labeling menu
#iterrows() returns the rows of the dataframe along with the index

def label_comments_menu(df):

    print("Creating manual labeling menu...\n")

    for i, row in df.iterrows():
        
        if pd.isna(row["isBot"]):

            print("\nComment:")
            print(row["comment_text"])
            print("\nLabel this comment:")
            print("  1 = Bot")
            print("  0 = Human")
            print("  s = Skip")
            print("  q = Quit")

            choice = input("Your choice: ").strip().lower()

            if choice == "q":
                print("Stopping manual labeling process...")
                break
            
            if choice == "s":
                continue

            if choice in ["0", "1"]:
               print("Labeling comment...")
               df.at[i, "isBot"] = int(choice)
            else:
                print("Invalid input...")
    
    return df
            











