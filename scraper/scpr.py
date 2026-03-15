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
job_links = set()  # use a set to avoid duplicates

page = 1
TARGET_JOBS = 150  # stop when we reach 150 jobs

print("Starting scraping jobs from Himalayas...")

while len(job_links) < TARGET_JOBS:
    URL = f"{BASE}/jobs/countries/{COUNTRY}?page={page}"
    print(f"Scraping page {page} ...")

    res = requests.get(URL, headers=headers)
    if res.status_code != 200:
        print(f"Failed to fetch page {page}, status code:", res.status_code)
        break

    soup = BeautifulSoup(res.text, "html.parser")
    
    # collect job links on this page
    links_found = 0
    for a in soup.select("article a[href*='/companies/']"):
        link = a.get("href")
        if link and "/jobs/" in link:
            full_url = BASE + link.split("?")[0]
            if full_url not in job_links:
                job_links.add(full_url)
                links_found += 1

    print(f"Found {links_found} new jobs on page {page}")
    
    if links_found == 0:  # no more jobs found → stop
        break

    page += 1
    time.sleep(1)  # polite delay

print(f"Total job links collected: {len(job_links)}")


def scrape_job(url):
    r = requests.get(url, headers=headers)
    soup = BeautifulSoup(r.text, "html.parser")

    data = {}

    title = soup.find("h1")
    data["title"] = title.get_text(strip=True) if title else None

    company = soup.select_one("a[href^='/companies/']")
    data["company"] = company.get_text(strip=True) if company else None

    description_block = soup.select_one("main")
    data["description"] = description_block.get_text(" ", strip=True) if description_block else None

    data["url"] = url

    info_section = soup.select_one("section.mt-8")
    if info_section:

        apply_before = info_section.find("h3", string="Apply before")
        if apply_before:
            data["apply_before"] = apply_before.find_next("time").get_text(strip=True)

        posted_on = info_section.find("h3", string="Posted on")
        if posted_on:
            data["posted_on"] = posted_on.find_next("time").get_text(strip=True)

        job_type = info_section.find("h3", string="Job type")
        if job_type:
            data["job_type"] = job_type.find_next("p").get_text(strip=True)

        salary = info_section.find("h3", string="Salary")
        if salary:
            data["salary"] = salary.find_next("p").get_text(strip=True)

        location_req = info_section.find("h3", string="Location requirements")
        if location_req:
            data["location_requirements"] = location_req.find_next("p").get_text(strip=True)

        exp = info_section.find("h3", string="Experience level")
        if exp:
            data["experience_level"] = [
                x.get_text(strip=True)
                for x in exp.find_next("div").select("div")
            ]

        location = info_section.find("h3", string="Location")
        if location:
            data["location"] = location.find_next("p").get_text(strip=True)

    categories = []
    cat_block = soup.find("h3", string="Job categories")
    if cat_block:
        for a in cat_block.find_next("div").select("a"):
            categories.append(a.get_text(strip=True))
    data["categories"] = categories

    skills = []
    skill_block = soup.find("h3", string="Skills")
    if skill_block:
        for a in skill_block.find_next("div").select("a"):
            skills.append(a.get_text(strip=True))
    data["skills"] = skills

    return data


# scrape each job link
for idx, link in enumerate(job_links, start=1):
    try:
        job = scrape_job(link)
        jobs.append(job)
        print(f"[{idx}/{len(job_links)}] Scraped: {job['title']}")
        time.sleep(1)  # polite delay
    except Exception as e:
        print("Error scraping:", link, e)


# save to JSON
with open("jobs_raws.json", "w", encoding="utf-8") as f:
    json.dump(jobs, f, indent=4, ensure_ascii=False)

print(f"Saved {len(jobs)} jobs to jobs_raws.json")