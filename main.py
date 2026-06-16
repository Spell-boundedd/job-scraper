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

for job in job_titles:
    link = job.find("a")

    if link:
        text = link.text

        company = text.split(" Is Hiring")[0]
        company = company.split(" is hiring")[0]

        jobs.append({
        "Company": company,
        "Job Title": text,
        "Link": link["href"]
    })

df = pd.DataFrame(jobs)

print(df.head(10))

df.to_csv(f"data/jobs_{timestamp}.csv", index=False)

print(f"\nSaved {len(df)} jobs to data/jobs_{timestamp}.csv")