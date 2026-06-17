import streamlit as st
import pandas as pd
import glob

st.title("Startup Job Analytics Dashboard")

st.caption(
    "Live job listings scraped from Hacker News Jobs"
)

csv_files = glob.glob("data/*.csv")



latest_file = max(csv_files)

df = pd.read_csv(latest_file)
search = st.text_input("Search Job Titles")

if search:
    df = df[df["Job Title"].str.contains(search, case=False, na=False)]
company_filter = st.selectbox(
    "Filter by Company",
    ["All"] + sorted(df["Company"].unique())
)

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

st.subheader("Top Hiring Companies")

top_companies = df["Company"].value_counts()

st.bar_chart(top_companies.head(10))