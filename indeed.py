# Scrape Indeed according to this tutorial: https://medium.com/@msalmon00/web-scraping-job-postings-from-indeed-96bd588dcb4b

import requests
import bs4
from bs4 import BeautifulSoup
import pandas as pd
import time


def extract_job_title_from_result(soup): 
    jobs = []
    for div in soup.find_all(name="div", attrs={"class":"result"}):
        titles = div.find_all(name="a", attrs={"data-tn-element":"jobTitle"})
        for title in titles:
            jobs.append(title["title"])
    return(jobs)

def extract_company_from_result(soup): 
    companies = []
    for div in soup.find_all(name="div", attrs={"class":"row"}):
        company = div.find_all(name="span", attrs={"class":"company"})
        if len(company) > 0:
            for b in company:
                companies.append(b.text.strip())
        else:
            sec_try = div.find_all(name="span", attrs={"class":"result-link-source"})
            for span in sec_try:
                companies.append(span.text.strip())
    return(companies)

def extract_location_from_result(soup): 
    locations = []
    spans = soup.findAll("span", attrs={"class": "location"})
    for span in spans:
        locations.append(span.text)
    return(locations)

def extract_salary_from_result(soup): 
    salaries = []
    for div in soup.find_all(name="div", attrs={"class":"row"}):
        try:
            salaries.append(div.find("nobr").text)
        except:
            try:
                div_two = div.find(name="div", attrs={"class":"sjcl"})
                div_three = div_two.find("div")
                salaries.append(div_three.text.strip())
            except:
                salaries.append("Nothing_found")
    return(salaries)

def extract_summary_from_result(soup): 
    summaries = []
    spans = soup.findAll("span", attrs={"class": "summary"})
    for span in spans:
        summaries.append(span.text.strip())
    return(summaries)

def main():
    #url = "https://www.indeed.com/jobs?q=data+scientist&l={}&start=10".format("Boston")
    #conducting a request of the stated URL above:
    #page = requests.get(url)
    
    #specifying a desired format of "page" using the html parser - this allows python to read the various components of the page, rather than treating it as one long string.
    #soup = BeautifulSoup(page.text, "html.parser")

    #printing soup in a more structured tree format that makes for easier reading
    #print(soup.prettify())
    
    #print extract_job_title_from_result(soup)
    #print extract_company_from_result(soup)
    #print extract_salary_from_result(soup)
    #print extract_location_from_result(soup)
    #print extract_summary_from_result(soup)
    
    # make table
    max_results_per_city = 10
    city_set = ["New+York","Chicago","San+Francisco", "Austin", "Seattle", "Los+Angeles", "Philadelphia", "Atlanta", "Dallas", "Pittsburgh", "Portland", "Phoenix", "Denver", "Houston", "Miami", "Washington+DC", "Boulder"]
    columns = ["city", "job_title", "company_name", "location", "summary", "salary"]
    sample_df = pd.DataFrame(columns = columns)
    
    job_title = []
    company_name = []
    location = []
    summary = []
    salary = []
    start=10
    for city in city_set:
        for start in range(0, max_results_per_city, 10):
            url = "https://www.indeed.com/jobs?q=data+scientist&l={}&start=10".format(city)
            page = requests.get(url)
            soup = BeautifulSoup(page.text, "html.parser")
            
            job_title = job_title + extract_job_title_from_result(soup)
            company_name = company_name + extract_company_from_result(soup)
            salary = salary + extract_salary_from_result(soup)
            location = location + extract_location_from_result(soup)
            summary = extract_summary_from_result(soup)
            
            time.sleep(1)  #ensuring at least 1 second between page grabs
    
    #TODO: Fix error - the arrays don't have the same length
    print len(job_title)
    print len(company_name)
    print len(location)
    print len(summary)
    print len(salary)
    jobslist = pd.DataFrame(
    {
     'job_title': job_title,
     'company_name': company_name,
     'salary': salary,
     'location': location,
     'summary': summary,
    })
    print jobslist
    
    
if __name__== "__main__":
    main()