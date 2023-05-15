from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup
import requests
import pandas as pd
import re
import math
import time
import json

# return pdInfo, reviews
def scrape_amazon_data(amazonUrl, cookie, bOnlyProductInformation = False):

    # URL = "https://www.amazon.com/RK-ROYAL-KLUDGE-Mechanical-Ultra-Compact/dp/B089GN2KBT/ref=sr_1_1_sspa?crid=1NNFWPEF3MEYM&keywords=gaming+keyboard&qid=1677243455&sprefix=gaming+keyboar%2Caps%2C282&sr=8-1-spons&psc=1&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUEyWEcyQU5DMzUwRThRJmVuY3J5cHRlZElkPUEwMDYwNjI1MVpPVE1ZRDhJQUhJVyZlbmNyeXB0ZWRBZElkPUEwMjk5ODQ3M0pSOVVNQ08wT1dPSiZ3aWRnZXROYW1lPXNwX2F0ZiZhY3Rpb249Y2xpY2tSZWRpcmVjdCZkb05vdExvZ0NsaWNrPXRydWU="
    URL = amazonUrl
    # URL = "https://www.amazon.com/GreenPan-CC000675-001-Valencia-Toxin-Free-Dishwasher/dp/B071HVQL76/ref=cm_cr_arp_d_pdt_img_top?ie=UTF8&th=1"
    HEADERS = {
        # "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko  ) Chrome/58.0.3029.110 Safari/537.3",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36",
        # "Cookie": f'{cookie}'
        "Cookie": 'session-id=137-3946308-0797720; ubid-main=131-8483923-0643914; lc-main=en_US; sp-cdn="L5Z9:IL"; skin=noskin; x-main="8MnZMlFP2DwLvKR0qOOGUaq?ipQ8mFn2i?WX3kyACVhkFll7D6LiWCOkntbz@oXZ"; at-main=Atza|IwEBII2-6IahHnJ1ySsluZ81Za09Th9SyDH3PQP8gw0-47gJGNP0iQFXukkpsgkdz3aLJ8sVHCGr6KRVYx2T1Ex7G4ormGKaDOp0zbFTbh-KhyLkCQfX9XvlS7CQo-5Pln9p0HTD6zZbhYIRhTKDcJs8gPBmFkSFfF40vZGj1XlyVOzu0mvrs3C6lrEUfD1RBA7Jq2eDbqTG5KbrsoTekE-4zxAb; sess-at-main="oqeEU+iNVZpV33K+Ktm53McCenDrSV5MluofSkIYFbM="; sst-main=Sst1|PQHnEkSBv01zfLi6WrPdakqrCSekO2_TVz2s6n8K0zVtvn4bSzjlSirnbOQRPIBKJDN5j1DjZTdEJONvFOLKVEbn26eb9WNHB5IJT8nwycVQbEeAzhV1TsW7Hm4NoqJf4vIw91sSyBKWosa-Xk-9Ve5rrjJsZES02dgIU2TKb_Vyo8FZfoHuOT3lj9HyYGjvML1u8dVkdvhNAaseb1AsruFUqrjU5dMFEGh38Hr_pWj3AKsqXJ5C_-5e8LRNCcCeBxlcVMJz4xtPUihG5F_LRjVu3pdiQ0Eh7jF38iu2vaRL4ys; session-id-time=2082787201l; i18n-prefs=USD; session-token=eIcF9DbXNOgky2f9DMyBSVpWugufAxVYUqERIgjI9VZWyKvjlp3WRbnf3VsJs5ekxZ+083sU/yU4xJkRZ8XgsOss8sWYGJ+TZdCN9iS+kEFKagEuhPt8+a484W3ladxitCOszI0GYvD/y4mkno5OzbQQ2Oub9BRcn7taqOvPuJZ9hDzcGXNugozDpH9etELX3g6Yh/SOlhG40/NLPsaC4Gew047lgyccXt1QnzAo2tq/HT6jnj+o9/8lfFl+3HkW; csm-hit=tb:s-ZBZND86MFYF0RYXM3E8J|1679411973809&t:1679411973901&adb:adblk_no'
    }

    # response = requests.get(URL, headers=HEADERS)
    response = requests.get(URL, headers=HEADERS)

    # print(response.content)
    
    # destFile = open('data.txt', 'w', -1)
    # destFile.write(f'data {response.content}')
    # destFile.close()

    soup = BeautifulSoup(response.content, "html.parser")

    see_all_reviews_link = soup.find("a", {"data-hook": "see-all-reviews-link-foot"})["href"]

    URL_ALL_REVIEWS="https://www.amazon.com/"+see_all_reviews_link


    response = requests.get(URL_ALL_REVIEWS, headers=HEADERS)

    soup = BeautifulSoup(response.content, "html.parser")


    # Find the element that contains the ratings with reviews and extract the text
    ratings_with_reviews_elem = soup.find("div", {"id": "filter-info-section"})
    ratings_with_reviews_text = ratings_with_reviews_elem.get_text().strip()
    
    #get just the reviews amount (\d+)\.(\d+)
    reviews_count = re.search(r'(\d+,\d+|\d+) with reviews', ratings_with_reviews_text).group(1)
    print(reviews_count)
    ratings_count = re.search(r'(\d+,\d+|\d+) total ratings', ratings_with_reviews_text).group(1)
    print(ratings_count)

    # get rating and product information
    title_elem = soup.find("a", {"data-hook": "product-link"})
    title = title_elem.get_text().strip()

    start_elem = soup.find("span", {"data-hook": "rating-out-of-text"})
    stars = start_elem.get_text().strip().split(' ')[0]

    img_elem = soup.find("img", {"data-hook": "cr-product-image"})
    img = img_elem.attrs['src']

    newProdInfo = { "rating" : ratings_count.replace(",", ""), "title": title, "stars": stars, "reviews": reviews_count.replace(",", ""), "img": img }
    
    print( "Product Information", newProdInfo )

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

    if bOnlyProductInformation == True:
        return newProdInfo
    else:
        with ThreadPoolExecutor() as executor:
            page_num=math.ceil(float(reviews_count.replace(",",""))/10)
            pages = [f"{URL_ALL_REVIEWS}&pageNumber={i+1}" for i in range(page_num)]
            results = executor.map(get_reviews, pages)
            for result in results:
                data += result

    print( "Get reviews", len(data) )

    return newProdInfo, data

# scrape_review('https://www.amazon.com/Dowinx-Headrest-Ergonomic-Computer-Footrest/dp/B09WTM88B6/ref=sr_1_1_sspa?keywords=gaming+chairs&pd_rd_r=a80345fe-4ba9-4d05-b12e-4a8c8b6c6b0f&pd_rd_w=WZSbW&pd_rd_wg=74sKp&pf_rd_p=12129333-2117-4490-9c17-6d31baf0582a&pf_rd_r=GBD3SGATVP87YRG752JB&qid=1683238168&sr=8-1-spons&psc=1&spLa=ZW5jcnlwdGVkUXVhbGlmaWVyPUFPNlgxQjFNVTdaS1omZW5jcnlwdGVkSWQ9QTA3MzI3OTIzSEQ4TDRFQTFEREdIJmVuY3J5cHRlZEFkSWQ9QTA1MzAyNzUzTElZMENNNDFBRlZOJndpZGdldE5hbWU9c3BfYXRmJmFjdGlvbj1jbGlja1JlZGlyZWN0JmRvTm90TG9nQ2xpY2s9dHJ1ZQ==',
            #   'session-id-time=2082787201l;i18n-prefs=USD;sp-cdn="L5Z9:IN";session-id=142-5381513-7931340;ubid-main=130-5831900-5055810;lc-main=en_US;skin=noskin;aws-mkto-trk=id%3A112-TZM-766%26token%3A_mch-aws.amazon.com-1682502400127-48496;aws_lang=en;aws-target-data=%7B%22support%22%3A%221%22%7D;AMCVS_7742037254C95E840A4C98A6%40AdobeOrg=1;aws-target-visitor-id=1683225430390-703973.31_0;s_cc=true;AMCV_7742037254C95E840A4C98A6%40AdobeOrg=1585540135%7CMCIDTS%7C19482%7CMCMID%7C88546971731933073101653767113569453729%7CMCAAMLH-1683830231%7C12%7CMCAAMB-1683830231%7CRKhpRz8krg2tLO6pguXWp5olkAcUniQYPHaMWWgdJ3xzPWQmdj0y%7CMCOPTOUT-1683232631s%7CNONE%7CMCAID%7C3224D159A07F3916-4000179C9BAECB73%7CvVersion%7C4.4.0;s_eVar60=ha%7Cacq_aws_takeover-1st-visit-devcnt%7Cawssm-evergreen-1st-visit%7Ced%7Cha_awssm-evergreen-1st-visit;aws-ubid-main=123-6253471-4282532;remember-account=false;aws-account-alias=227843703052;aws-userInfo=%7B%22arn%22%3A%22arn%3Aaws%3Aiam%3A%3A227843703052%3Auser%2Fintelman1128%40gmail.com%22%2C%22alias%22%3A%22227843703052%22%2C%22username%22%3A%22intelman1128%2540gmail.com%22%2C%22keybase%22%3A%22YcMHiy5NFMuK%2FwwEooM1i4ITT5rH8Ldsb7zWUXln%2BNY%5Cu003d%22%2C%22issuer%22%3A%22http%3A%2F%2Fsignin.aws.amazon.com%2Fsignin%22%2C%22signinType%22%3A%22PUBLIC%22%7D;aws-userInfo-signed=eyJ0eXAiOiJKV1MiLCJrZXlSZWdpb24iOiJ1cy1lYXN0LTEiLCJhbGciOiJFUzM4NCIsImtpZCI6IjhmMjE5MWY4LTRlMmEtNDlmZS04NGMzLWE4NTMzNzBjYjIzNyJ9.eyJzdWIiOiIyMjc4NDM3MDMwNTIiLCJzaWduaW5UeXBlIjoiUFVCTElDIiwiaXNzIjoiaHR0cDpcL1wvc2lnbmluLmF3cy5hbWF6b24uY29tXC9zaWduaW4iLCJrZXliYXNlIjoiWWNNSGl5NU5GTXVLXC93d0Vvb00xaTRJVFQ1ckg4TGRzYjd6V1VYbG4rTlk9IiwiYXJuIjoiYXJuOmF3czppYW06OjIyNzg0MzcwMzA1Mjp1c2VyXC9pbnRlbG1hbjExMjhAZ21haWwuY29tIiwidXNlcm5hbWUiOiJpbnRlbG1hbjExMjglNDBnbWFpbC5jb20ifQ.IrZN2utPfCidlw0rxX_YVrfZGOodtsgEdS7p3heCaWFhv9QCflew2qNSkflfvh4xECd_bf0HwLqmK6if5RbBiAL13awVE9hET4o1mw77CWAOUBmKe8b4GzWv-yOU4yUc;regStatus=registered;noflush_awsccs_sid=bc97de05fb4867afef9b8860f970a0103fa17e4f1c213712dbe218e7ef4ea945;aws-signer-token_us-east-1=eyJrZXlWZXJzaW9uIjoiTnRjYnQxZmJkUjJraGh0cVpqaEtYV2l1a1BhbkVWME4iLCJ2YWx1ZSI6IjRyNWtrM04rdmxYRXhJNXdHamZSYlkrWi9WOHo0a0lvemZHZ0hPL0FuTmc9IiwidmVyc2lvbiI6MX0=;s_sq=%5B%5BB%5D%5D;session-token="2YIc80fG7lq4p4xKtiaN9AUJD80lPZSwYfIbXXS7eVoJQxRcs5Z0YOzarn+j9F/g6IBzWF8nc8/+Mh5rpDd36yfoO/VsGhAeJr/Qn5n1dRZNn4e8+CxvtAUiIZwe/zU7YZ9PO7cS9e4cbo1m9Y5jKSBeHfrBOCwHayaXNGq0nY6Y9GxyJwYAePTaBSXNOJ/agg/nW8KmpOQwVS4i2X/rPk6BRZo8D81j5hN+RTaP3xA=";csm-hit=tb:s-MVCNS44389CF6MMY23W2|1683238197841&t:1683238231410&adb:adblk_no;')