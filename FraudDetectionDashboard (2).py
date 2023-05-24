import streamlit as st
import praw
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Reddit API credentials
client_id = '72c4P3tYr2Cl1j-V-QliXQ'
client_secret = 'xqnsYo0fMTHNx-I2lm8Y92eNBMuPew'
user_agent = 'Streamlit_visual'

# Connect to Reddit API
reddit = praw.Reddit(client_id=client_id, client_secret=client_secret, user_agent=user_agent)

# Streamlit App
st.set_page_config(page_title="Data Visualization Dashboard", page_icon=":guardsman:", layout="wide")
st.markdown(
    """
    <style>
    .stApp {
        background-color: #f0f0f0;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Collect and process posts
def collect_and_process_posts(keywords, limit=50):
    posts = []
    for keyword in keywords:
        subreddit_posts = reddit.subreddit('all').search(keyword, limit=limit)
        for post in subreddit_posts:
            posts.append([post.title, post.author.name, post.subreddit.display_name, post.created_utc])
    df = pd.DataFrame(posts, columns=['Title', 'Author', 'Subreddit', 'Timestamp'])
    df['Timestamp'] = pd.to_datetime(df['Timestamp'], unit='s')
    return df

# Analyze the data and create visualizations
def analyze_data(df):
    st.subheader("Fraud Mentions by Subreddit")
    subreddit_counts = df['Subreddit'].value_counts().head(10)
    st.bar_chart(subreddit_counts)

    st.subheader("Fraud Mentions Over Time")
    daily_counts = df.set_index('Timestamp').resample('D').size()
    st.line_chart(daily_counts)

# Main function to run the Streamlit app
def main():
    keywords = ['telecoms fraud', 'telecoms scam', 'phone fraud', 'billing fraud', 'identity theft']
    df = collect_and_process_posts(keywords)
    st.title("Fraud Posts")
    st.dataframe(df)
    analyze_data(df)

if __name__ == '__main__':
    main()
