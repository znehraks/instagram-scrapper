import os
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep
from bs4 import BeautifulSoup
from pathos.multiprocessing import ProcessPool as Pool
import time
import io
import sys
# sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf8')
# sys.stderr = io.TextIOWrapper(sys.stdout.detach(), encoding='utf8')

# 혹은 전체적으로 그림만 훑어서 이미지 정보 획득 기능을 추가.
# selenium으로 정보 모으고 => opencv로 이미지 분석.

# -----------------------------------------------------------
# multiprocessing으로 속도개선 (실시간 활용까지 고려)
# -----------------------------------------------------------

# pageString = crawl()
# postInfos = parse(pageString)
# pageSources = postCrawl(postInfos)
# list = getHashTags(pageSources)
# for i in list:
#     print(i)

# getHashTags(postCrawl(parse(crawl())))


# SCROLL_PAUSE_TIME = 0.5
# # Get scroll height
# last_height = driver.execute_script("return document.body.scrollHeight")

# while True:
#     # Scroll down to bottom
#     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

#     # Wait to load page
#     time.sleep(SCROLL_PAUSE_TIME)

#     # Calculate new scroll height and compare with last scroll height
#     new_height = driver.execute_script("return document.body.scrollHeight")
#     if new_height == last_height:
#         break
#     last_height = new_height


# 본 코드 --------------------------------------------------------------------

sys.stdout.reconfigure(encoding='utf-8')


def parse(pageString):
    bsObj = BeautifulSoup(pageString, "html.parser")
    posts = bsObj.findAll("div", {"class": "KL4Bh"})
    images = []
    for post in posts:
        images.append(post.find("img")["src"])
    return images


def crawl(keyword):
    chrome_options = Options()
    driver = webdriver.Chrome(
        executable_path="C:\\Users\\USER\\Desktop\\Store\\chromedriver\\chromedriver.exe",
        options=chrome_options
    )
    url = f"https://www.instagram.com/explore/tags/{keyword}/?hl=ko"
    print(url)
    driver.get(url)  # 주소입력하고 enter치는것

# ...........................................................
    SCROLL_PAUSE_TIME = 1.6
    count = 0
    while count != 10:
        # Get scroll height
        last_height = driver.execute_script(
            "return document.body.scrollHeight")
        # Scroll down to bottom
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")
        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)
        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height
        count += 1
# .................................................................

    sleep(2)
    pageString = driver.page_source
    # print(pageString)
    # return True
    # 인스타 껍데기
    # 인스타 내용 <div class = "Nnq7C aaa">
    driver.close()
    return pageString


keyword = input("크롤링할 검색어 입력해라: ")
pageString = crawl(keyword)
images = parse(pageString)
for i in images:
    print(i)

# if __name__ == "__main__":
#     pool = Pool(processes=4)
#     list = pool.map(getHashTags, postCrawl(parse(crawl())))
#     for i in list:
#         print(i)

# getHashTags(postCrawl(parse(crawl())))
