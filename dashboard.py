import streamlit as st
import pandas as pd
import glob

st.title("Job Market Dashboard")

csv_files = glob.glob("data/*.csv")

latest_file = max(csv_files)

df = pd.read_csv(latest_file)

st.write("Latest Scraped Jobs")
st.dataframe(df)

st.subheader("Top Hiring Companies")

top_companies = df["Company"].value_counts()

st.bar_chart(top_companies.head(10))