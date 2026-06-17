import streamlit as st
import pandas as pd
import glob

st.title("Job Market Dashboard")

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
st.dataframe(df)

st.subheader("Top Hiring Companies")

top_companies = df["Company"].value_counts()

st.bar_chart(top_companies.head(10))