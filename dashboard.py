import streamlit as st
import pandas as pd
import glob
from collections import Counter
st.sidebar.title("Controls")
st.title("Startup Job Analytics Dashboard")

st.caption(
    "Live job listings scraped from Hacker News Jobs"
)

csv_files = glob.glob("data/*.csv")



latest_file = max(csv_files)

df = pd.read_csv(latest_file)
st.write(f"Current dataset: {latest_file}")
search = st.sidebar.text_input("Search Job Titles")

company_filter = st.sidebar.selectbox(
    "Filter by Company",
    ["All"] + sorted(df["Company"].unique())
)
if search:
    df = df[df["Job Title"].str.contains(search, case=False, na=False)]

if company_filter != "All":
    df = df[df["Company"] == company_filter]
st.write("Latest Scraped Jobs")
col1, col2 = st.columns(2)

col1.metric(
    "Total Jobs",
    len(df)
)

col2.metric(
    "Companies",
    df["Company"].nunique()
)
st.data_editor(df)
csv = df.to_csv(index=False)

st.download_button(
    label="Download Filtered Data",
    data=csv,
    file_name="jobs.csv",
    mime="text/csv"
)


top_companies = df["Company"].value_counts().head(10)

st.subheader("Top 10 Hiring Companies")

st.bar_chart(top_companies)
words = []

for title in df["Job Title"]:
    words.extend(title.lower().split())

common_words = Counter(words)

st.subheader("Most Common Job Keywords")

keyword_df = pd.DataFrame(
    common_words.most_common(10),
    columns=["Keyword", "Count"]
)

st.dataframe(keyword_df)