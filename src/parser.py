"""Parser for extracting job data from Jobs.cz HTML."""
import re
from bs4 import BeautifulSoup
from datetime import datetime


def _extract_jobs(html):
    """Extract job listings from HTML."""
    if not html:
        return []
    
    soup = BeautifulSoup(html, 'html.parser')
    jobs = []
    
    # Jobs.cz uses <article> tags or similar for job cards
    # Adapting to their actual structure
    job_cards = soup.find_all('article') or soup.find_all('div', class_=re.compile(r'job|offer|card', re.I))
    
    if not job_cards:
        # Fallback: look for links to job detail pages
        links = soup.find_all('a', href=re.compile(r'/rpd/|/rph/|/job/', re.I))
        if links:
            # Extract from link-based structure
            for link in links:
                job = _extract_from_link(link)
                if job and job.get('title'):
                    jobs.append(job)
        return jobs
    
    for card in job_cards:
        job = {}
        
        # Title
        title_elem = card.find(['h2', 'h3', 'a'], class_=re.compile(r'title|name|position', re.I))
        if not title_elem:
            title_elem = card.find('a', href=re.compile(r'/rpd/|/job/'))
        job['title'] = title_elem.get_text(strip=True) if title_elem else None
        
        # URL
        link_elem = card.find('a', href=re.compile(r'/rpd/|/rph/|/job/'))
        if link_elem:
            href = link_elem.get('href', '')
            job['url'] = href if href.startswith('http') else f"https://www.jobs.cz{href}"
        else:
            job['url'] = None
        
        # Company
        company_elem = card.find(class_=re.compile(r'company|employer|firma', re.I))
        job['company'] = company_elem.get_text(strip=True) if company_elem else None
        
        # Location
        location_elem = card.find(class_=re.compile(r'location|place|mesto|lokace', re.I))
        job['location'] = location_elem.get_text(strip=True) if location_elem else None
        
        # Salary
        salary_elem = card.find(class_=re.compile(r'salary|wage|plat|mzda', re.I))
        job['salary'] = salary_elem.get_text(strip=True) if salary_elem else None
        
        # Job type
        jobtype_elem = card.find(class_=re.compile(r'type|contract|uvazek', re.I))
        job['jobType'] = jobtype_elem.get_text(strip=True) if jobtype_elem else None
        
        # Posted date
        date_elem = card.find(class_=re.compile(r'date|time|posted|vyveseno', re.I))
        job['postedDate'] = date_elem.get_text(strip=True) if date_elem else None
        
        # Category
        cat_elem = card.find(class_=re.compile(r'category|obor|kategorie', re.I))
        job['category'] = cat_elem.get_text(strip=True) if cat_elem else None
        
        # Description snippet
        desc_elem = card.find(class_=re.compile(r'description|snippet|text|popis', re.I))
        job['description'] = desc_elem.get_text(strip=True) if desc_elem else None
        
        job['scrapedAt'] = datetime.utcnow().isoformat() + 'Z'
        
        # Only add if we got at least a title
        if job.get('title'):
            jobs.append(job)
    
    return jobs


def _extract_from_link(link):
    """Extract job data from a job link element."""
    job = {}
    
    # Title from link text or parent structure
    job['title'] = link.get_text(strip=True)
    
    # URL
    href = link.get('href', '')
    job['url'] = href if href.startswith('http') else f"https://www.jobs.cz{href}"
    
    # Try to find parent container for more data
    parent = link.find_parent(['article', 'div', 'li'])
    if parent:
        # Company
        company = parent.find(class_=re.compile(r'company|employer', re.I))
        job['company'] = company.get_text(strip=True) if company else None
        
        # Location
        location = parent.find(class_=re.compile(r'location|place', re.I))
        job['location'] = location.get_text(strip=True) if location else None
        
        # Salary
        salary = parent.find(class_=re.compile(r'salary|wage', re.I))
        job['salary'] = salary.get_text(strip=True) if salary else None
    
    job['jobType'] = None
    job['postedDate'] = None
    job['category'] = None
    job['description'] = None
    job['scrapedAt'] = datetime.utcnow().isoformat() + 'Z'
    
    return job
