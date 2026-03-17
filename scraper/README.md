# AI Salary Predictor – Web Scraping Module

## Project Overview

This project is the **Web Scraping module** of the AI Salary Predictor assignment.  
Its purpose is to **collect job postings from a real job website** and save them in a structured JSON file for further processing (LangChain + Machine Learning modules).

The scraper collects the following fields from each job posting:

- `title` – Job title  
- `company` – Company name  
- `location` – Job location  
- `description` – Job description  
- `salary` – Salary if available (None if not listed)  

The scraper also implements **pagination** and **error handling** to collect **≥150 job records**.

---

## Technologies Used

- **Python 3.14**  
- **requests** – For making HTTP requests  
- **BeautifulSoup (bs4)** – For parsing HTML and extracting job data  
- **JSON** – For saving structured job data  

---

## How to Run

1. **Clone the repository** or navigate to your project folder:

```bash
cd C:\Users\DELL\Desktop\project1