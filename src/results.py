import pandas as pd


def create_results_dataframe(unlabelled_df, y_predict, y_probability):

    data = {
        "comment_text": unlabelled_df["comment_text"],
        "bot_label": y_predict,
        "bot_probability": y_probability
    }

    results = pd.DataFrame(data)

    return results

#sorting rearranges the rows, while keeping their original index numbers attached
def sort_by_probability(results_df):

    sorted_df = results_df.sort_values("bot_probability", ascending=False)

    return sorted_df




    

