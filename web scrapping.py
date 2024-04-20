import pandas as pd
import requests
from selenium import webdriver
from bs4 import BeautifulSoup
import time
import json

url = "https://www.dell.com/en-in/work/shop/business-laptop-notebook-computers/latitude-7440-laptop/spd/latitude-14-7440-2-in-1-laptop/n001l7440017in9_vp#ratings_section"
browser = webdriver.Firefox()
browser.get(url)
time.sleep(5)

html = browser.page_source
soup = BeautifulSoup(html, 'html.parser')
data = soup.find_all("script", type="application/ld+json")

result = []
for contents in data:
    jsonData = json.loads(contents.text)
    if "review" in jsonData:
        for review in jsonData["review"]:
            headline = review["headline"]
            review_body = review["reviewBody"]
            rating_value = review["reviewRating"]["ratingValue"]
            result.append({"headline": headline, "reviewBody": review_body, "ratingValue": rating_value})

for page_num in range(2, 12):
    
    url = f"https://www.dell.com/en-in/work/shop/business-laptop-notebook-computers/latitude-7440-laptop/spd/latitude-14-7440-2-in-1-laptop/n001l7440017in9_vp?bvstate=pg:{page_num}/ct:r#ratings_section"
    browser.get(url)
    time.sleep(5)  # Wait for the new content to load

    html = browser.page_source
    soup = BeautifulSoup(html, 'html.parser')
    data = soup.find_all("script", type="application/ld+json")

    for contents in data:
        jsonData = json.loads(contents.text)
        if "review" in jsonData:
            for review in jsonData["review"]:
                headline = review["headline"]
                review_body = review["reviewBody"]
                rating_value = review["reviewRating"]["ratingValue"]
                result.append({"headline": headline, "reviewBody": review_body, "ratingValue": rating_value})

url = "https://www.cnbctv18.com/technology/dell-latitude-7440-ultralight-review-a-solid-upgrade-for-professionals-and-creators-18689431.htm"

# Send a GET request to the URL
response = requests.get(url)
soup = BeautifulSoup(response.text, "html.parser")
results1 =[]
headline = soup.find('h1', class_='jsx-1947393162 narticle-title').get_text()
review_body = soup.find('h2', class_='jsx-3e3b1f1d81bd42bc narticle-intext').get_text()
results1.append({"headline": headline, "reviewBody": review_body})

url2 = 'https://www.notebookcheck.net/Dell-Latitude-7440-laptop-review-Beating-the-Latitude-9440-in-some-key-areas.732719.0.html'
response2 = requests.get(url2)
soup2 = BeautifulSoup(response2.text, "html.parser")
results2 = []
headline2 = soup2.find('h1', style='margin-bottom:0.3em')
review_body2 = soup2.find('p', class_='bodytext')
results2.append({"headline": headline2, "reviewBody": review_body2})

url3 = 'https://www.pcmag.com/articles/living-with-the-dell-latitude-7440-ultralight'
response3 = requests.get(url3)
soup3 = BeautifulSoup(response3.content, "html.parser")
results3 = []
headline3 = soup3.find('h1', class_='mb-4 font-featured text-4xl leading-tight tracking-wide md:text-5xl')
review_body3 = soup3.find('p')
results3.append({"headline": headline3, "reviewBody": review_body3})

results = result + results1 + results2 + results3   


df = pd.DataFrame(results)
df.to_csv('reviews.csv', index=False)