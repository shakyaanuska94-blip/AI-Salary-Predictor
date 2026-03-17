import requests
from bs4 import BeautifulSoup
import json
import time

BASE = "https://himalayas.app"
COUNTRY = "nepal"

headers = {
    "User-Agent": "Mozilla/5.0"
}

jobs = []
job_links = set()

page = 1
TARGET_JOBS = 150

print("Collecting job links...")

while len(job_links) < TARGET_JOBS:
    URL = f"{BASE}/jobs/countries/{COUNTRY}?page={page}"
    res = requests.get(URL, headers=headers)

    if res.status_code != 200:
        break

    soup = BeautifulSoup(res.text, "html.parser")

    for a in soup.select("article a[href*='/companies/']"):
        link = a.get("href")

        if link and "/jobs/" in link:
            full_url = BASE + link.split("?")[0]
            job_links.add(full_url)

    print("Page", page, "collected links:", len(job_links))

    page += 1
    time.sleep(1)


def scrape_job(url):

    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")

    data = {}

    title = soup.find("h1")
    data["job_title"] = title.get_text(strip=True) if title else None

    company = soup.select_one("a[href^='/companies/']")
    data["company"] = company.get_text(strip=True) if company else None

    location = soup.find("h3", string="Location")
    data["location"] = location.find_next("p").get_text(strip=True) if location else None

    salary = soup.find("h3", string="Salary")
    data["salary"] = salary.find_next("p").get_text(strip=True) if salary else None

    description = soup.select_one("main")
    data["description"] = description.get_text(" ", strip=True) if description else None

    return data


print("Scraping job details...")

for link in list(job_links)[:TARGET_JOBS]:
    try:
        job = scrape_job(link)
        jobs.append(job)

        print("Scraped:", job["job_title"])

        time.sleep(1)

    except Exception as e:
        print("Error:", link, e)


with open("jobs_raws.json", "w", encoding="utf-8") as f:
    json.dump(jobs, f, indent=4, ensure_ascii=False)

print("Saved to jobs_raws.json")