import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")
url = "https://news.ycombinator.com/jobs"

headers = {
    "User-Agent": "Mozilla/5.0"
}

response = requests.get(url, headers=headers)

print("Status Code:", response.status_code)

soup = BeautifulSoup(response.text, "html.parser")

jobs = []

job_titles = soup.find_all("span", class_="titleline")

job_rows = soup.find_all("tr", class_="athing submission")

for row in job_rows:

    titleline = row.find("span", class_="titleline")

    if titleline:
        link_tag = titleline.find("a")

        if link_tag:

            title = link_tag.text
            link = link_tag["href"]

            company = title.split(" Is Hiring")[0]
            company = company.split(" is hiring")[0]

            company = company.split("(")[0].strip()

            next_row = row.find_next_sibling("tr")

            age = "Unknown"

            if next_row:
                age_tag = next_row.find("span", class_="age")

                if age_tag:
                    age = age_tag.text

            jobs.append({
                "Company": company,
                "Job Title": title,
                "Posted": age,
                "Link": link
            })

df = pd.DataFrame(jobs)

print(df.head(10))

df.to_csv(f"data/jobs_{timestamp}.csv", index=False)

print(f"\nSaved {len(df)} jobs to data/jobs_{timestamp}.csv")
print("\nTop Companies Hiring:\n")

top_companies = df["Company"].value_counts()

print(top_companies.head(10))