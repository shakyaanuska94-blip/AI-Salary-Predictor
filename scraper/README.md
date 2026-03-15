# AI-Salary-Predictor
# AI Salary Predictor – Web Scraping Module

## Overview
This module collects job postings from a sample website and stores the data in JSON format.  
It is the first step of the AI Salary Predictor project pipeline, which will later process the data using LangChain and train a machine learning model to predict salaries.

---

## Features
- Scrapes job postings from the selected website.
- Extracts the following information for each job:
  - Job title
  - Company name
  - Location
  - Job description
  - Salary (if available)
- Stores raw job data in a JSON file (`jobs_raw.json`).
- Handles missing fields and avoids duplicate records.
- Implements pagination to scrape multiple pages.

---

## How to Run
1. Make sure Python is installed (version 3.8+ recommended).  
2. Install required libraries:

```bash
pip install requests beautifulsoup4