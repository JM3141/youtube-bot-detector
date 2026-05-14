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

    #finding the first row that has not been labelled
    start_index = df[df["isBot"].isna()].index.min()

    #condition for if all rows have been labelled
    if pd.isna(start_index):
        print("All comments are already labelled")
        return df

    for i in range(start_index, len(df)):
        
        if pd.isna(df.at[i, "isBot"]):

            print("\nComment:")
            print(df.at[i, "comment_text"])
            print("\nLabel this comment:")
            print("  1 = Bot")
            print("  0 = Human")
            print("  s = Skip")
            print("  q = Quit")

            choice = input("\nYour choice: ").strip().lower()

            if choice == "q":
                print("\nStopping manual labeling process...")
                df.to_csv("datasets/labeled.csv", index=False)
                print("Progress Saved.")
                break
            
            if choice == "s":
                continue

            if choice in ["0", "1"]:
               print("Labeling comment...")
               df.at[i, "isBot"] = int(choice)
               print("Label saved.")
               df.to_csv("datasets/labeled.csv", index=False)
               print("process complete.")
            else:
                print("Invalid input...")
    
    return df
            











