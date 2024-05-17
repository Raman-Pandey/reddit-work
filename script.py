from IPython import display
import streamlit as st
import math
from pprint import pprint
import pandas as pd
import numpy as np
import nltk
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(style='darkgrid', context='talk', palette='Dark2')
import praw

reddit = praw.Reddit(client_id='KgFBUmRPl1whtw',
                     client_secret='gmOJmuS3iDRwrUnhmn0CYtpnGGY',
                     user_agent='LearnDataSci')
def collect_comments_and_replies(submission):
    """Collect comments and directly associated replies."""
    data_list = []
    submission.comments.replace_more(limit=1000)  # Load all comments and remove MoreComments
    
    for comment in submission.comments.list():
        comment_data = {
            "post_id": submission.id,
            "author": str(submission.author),
            "url": submission.url,
            "title": submission.title,
            "comment_id": comment.id,
            "comment_body": comment.body,
            "comment_author": str(comment.author),
            "reply_body": ""
        }
        
        comment.replies.replace_more(limit=0)
        for reply in comment.replies:
            reply_data = comment_data.copy()
            reply_data['reply_body'] = reply.body
            data_list.append(reply_data)

        if not comment.replies:
            data_list.append(comment_data)

    return data_list

def extract_subreddit_posts(subreddit_name, limit=10):
    all_data = []
    subreddit = reddit.subreddit(subreddit_name)
    for submission in subreddit.hot(limit=limit):
        all_data.extend(collect_comments_and_replies(submission))

    return pd.DataFrame(all_data)

# Streamlit interface
st.title('Reddit Subreddit Scraper')
subreddit_name = st.text_input("Enter Subreddit Name", "python")
limit = st.number_input("Number of Posts to Scrape", min_value=1, max_value=100, value=10)

if st.button("Scrape"):
    data_df = extract_subreddit_posts(subreddit_name, limit)
    st.write(data_df)
    csv = data_df.to_csv(index=False).encode('utf-8')
    st.download_button("Download CSV", csv, "comments_and_replies.csv", "text/csv", key='download-csv')