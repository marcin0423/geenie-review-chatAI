from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup
import requests
import pandas as pd
import re
import math
import time

def scrape_review(amazonUrl, cookie):

    print(amazonUrl, cookie)
    # URL = "https://www.amazon.com/RK-ROYAL-KLUDGE-Mechanical-Ultra-Compact/dp/B089GN2KBT/ref=sr_1_1_sspa?crid=1NNFWPEF3MEYM&keywords=gaming+keyboard&qid=1677243455&sprefix=gaming+keyboar%2Caps%2C282&sr=8-1-spons&psc=1&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUEyWEcyQU5DMzUwRThRJmVuY3J5cHRlZElkPUEwMDYwNjI1MVpPVE1ZRDhJQUhJVyZlbmNyeXB0ZWRBZElkPUEwMjk5ODQ3M0pSOVVNQ08wT1dPSiZ3aWRnZXROYW1lPXNwX2F0ZiZhY3Rpb249Y2xpY2tSZWRpcmVjdCZkb05vdExvZ0NsaWNrPXRydWU="
    URL = amazonUrl
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
        "Host": "www.amazon.com",
        "Accept-Encoding": "gzip, deflate",
        "Cookie": cookie
    }    

    response = requests.get(URL, headers=HEADERS)

    soup = BeautifulSoup(response.content, "html.parser")

    # print(response.content)

    see_all_reviews_link = soup.find("a", {"data-hook": "see-all-reviews-link-foot"})["href"]

    print("https://www.amazon.com/"+see_all_reviews_link)

    URL_ALL_REVIEWS="https://www.amazon.com/"+see_all_reviews_link


    response = requests.get(URL_ALL_REVIEWS, headers=HEADERS)

    soup = BeautifulSoup(response.content, "html.parser")


    # Find the element that contains the ratings with reviews and extract the text
    ratings_with_reviews_elem = soup.find("div", {"id": "filter-info-section"})
    ratings_with_reviews_text = ratings_with_reviews_elem.get_text().strip()

    print(ratings_with_reviews_text)

    #get just the reviews amount (\d+)\.(\d+)
    reviews_count = re.search(r'(\d+,\d+|\d+) with reviews', ratings_with_reviews_text).group(1)

    print(reviews_count)

    data = []

    def scrape_reviews(page_url):
        response = requests.get(page_url, headers=HEADERS)

        soup = BeautifulSoup(response.content, 'html.parser')

        reviews = soup.find_all('div', {'data-hook': 'review'})
        page_data = []
        for review in reviews:
            profile_name = review.find("span", {"class": "a-profile-name"}).get_text()
            title_elem = review.find("a", {"data-hook": "review-title"})
            title = title_elem.get_text().strip() if title_elem else ""
            body = review.find("span", {"data-hook": "review-body"}).get_text().strip()
            stars_elem = review.find("i", {"data-hook": "review-star-rating"})
            stars = float(stars_elem.span.get_text().split()[0]) if stars_elem and stars_elem.span else None
            page_data.append([profile_name, title, body, stars])

        return page_data

    with ThreadPoolExecutor() as executor:
        page_num=math.ceil(float(reviews_count.replace(",",""))/10)
        pages = [f"{URL_ALL_REVIEWS}&pageNumber={i+1}" for i in range(page_num)]
        results = executor.map(scrape_reviews, pages)
        for result in results:
            data += result

    print( "Get reviews", len(data) )

    return data