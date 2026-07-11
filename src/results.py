import pandas as pd


def create_results_dataframe(unlabelled_df, y_predict, y_probability):

    data = {
        "comment_text": unlabelled_df["comment_text"],
        "bot_label": y_predict,
        "bot_probability": y_probability
    }

    results = pd.DataFrame(data)

    return results




    

