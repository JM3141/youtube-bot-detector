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

#function filters comments in dataframe that have a bot probability greater than or equal to 0.8
def filter_suspicious_comments(results_df, threshold=0.8):
    return results_df[results_df["bot_probability"] >= threshold]

#function provides summary statistics for all comments in the dataframe that are flagged as bots
def summary_metrics(results_df, threshold=0.8):
    total = len(results_df)
    flagged = (results_df["bot_probability"] >= threshold).sum()

    return {
        "total_comments": total,
        "flagged_comments": flagged,
        "flagged_ratio": flagged / total if total > 0 else 0
    }





    

