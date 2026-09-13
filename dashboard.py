import streamlit as st
import pandas as pd
from src.results import filter_suspicious_comments, summary_metrics

def run_dashboard(results_df):

    st.title("Youtube Bot Detector Dashboard")

    threshold = st.slider("Bot Probability Threshold", 0.6, 0.95, 0.8)

    metrics = summary_metrics(results_df, threshold)

    col1, col2, col3 = st.columns(3)

    col1.metric("Total Comments", metrics["total_comments"])
    col2.metric("Flagged Comments", metrics["flagged_comments"])
    col3.metric("Flagged Ratio", f"{metrics['flagged_ratio']*100:.2f}%")


    suspicious_df = filter_suspicious_comments(results_df, threshold)

    st.subheader("Suspicious Comments")
    st.dataframe(suspicious_df)







