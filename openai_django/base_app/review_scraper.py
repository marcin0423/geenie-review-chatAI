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
    # URL = "https://www.amazon.com/GreenPan-CC000675-001-Valencia-Toxin-Free-Dishwasher/dp/B071HVQL76/ref=cm_cr_arp_d_pdt_img_top?ie=UTF8&th=1"
    HEADERS = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko  ) Chrome/58.0.3029.110 Safari/537.3",
        "Host": "www.amazon.com",
        "Accept-Encoding": "gzip, deflate",
        # "Cookie": 'session-id-time=2082787201l;i18n-prefs=USD;sp-cdn="L5Z9:IN";session-id=142-5381513-7931340;ubid-main=130-5831900-5055810;lc-main=en_US;skin=noskin;session-token="uCSv3lK1Y/Qv0zhQEQSLfUijhyfHwNMFmPEHt/vTqGyaEDZvs5RqaiOOD6xLHeKKq2dTERn4b+plX2uDhIVQiF3bur5CjQT8U3Kx73E5e+7mC5wDdHATR5A61o/XGsUNPMpOHyNISqVVGjV9yZ6vN8a8mdv60HbM5V1GrPtzPAGOFZ0F89mGmyJd8Fnm5HpNXNcxdRPhmRMAULRJQtO5fk9B3S54vF9CX4FHd2/hPXw=";csm-hit=tb:ESA33AMNM8YG3HZRPD5N+s-SRB1CNQ7PJV0J0NEHHAS|1683203056788&t:1683203056788&adb:adblk_no;'
        "Cookie": f'{cookie}'
    }

    response = requests.get(URL, headers=HEADERS)

    soup = BeautifulSoup(response.content, "html.parser")

    see_all_reviews_link = soup.find("a", {"data-hook": "see-all-reviews-link-foot"})["href"]

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

    def get_reviews(page_url):
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
        results = executor.map(get_reviews, pages)
        for result in results:
            data += result

    print( "Get reviews", len(data) )

    return data