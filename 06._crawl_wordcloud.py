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
import wordCloud
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


def postCrawl(postInfos):
    chrome_options = Options()
    driver = webdriver.Chrome(
        executable_path="./chromedriver.exe",
        options=chrome_options
    )
    pageSources = []
    for postInfo in postInfos:
        url = postInfo["link"]
        driver.get(url)
        pageString = driver.page_source
        pageSources.append(pageString)
        # count += 1
        # if count > 1:
        #     break
    return pageSources


def getHashTags(pageSources):
    hashTagsList = []
    for pageSource in pageSources:
        bsObj = BeautifulSoup(pageSource, "html.parser")
        div = bsObj.find("div", {"class": "C4VMK"})
        span = div.find("span")
        # 댓글 두번째까진 받아서 해시태그 분석
        hashTags = span.findAll("a", {"class": "xil3i"})
        for hashTag in hashTags:
            hashTagsList.append(hashTag.string)
    return hashTagsList


def getPostInfo(post):
    aTag = post.find("a")
    link = "https://www.instagram.com{}".format(aTag['href'])
    return {"link": link}


def parse(pageString):
    bsObj = BeautifulSoup(pageString, "html.parser")
    posts = bsObj.findAll("div", {"class": "v1Nh3"})
    postInfos = []
    for post in posts:
        postInfo = getPostInfo(post)
        postInfos.append(postInfo)
    return postInfos


def crawl(keyword):
    chrome_options = Options()
    driver = webdriver.Chrome(
        executable_path="./chromedriver.exe",
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


keyword = input("마이닝할 검색어를 입력하세요: ")

# 결과로 쓰일 result.txt 열기
output_file_name = 'result.txt'
open_output_file = open(output_file_name, 'w', -1, "utf-8")

pageString = crawl(keyword)
postInfos = parse(pageString)
pageSources = postCrawl(postInfos)
list = getHashTags(pageSources)
# 결과 저장
for i in list:
    word = i.split('#')[1]
    open_output_file.write('{}\n'.format(word))
    print(word)
open_output_file.close()
wordCloud.main()
# if __name__ == "__main__":
#     pool = Pool(processes=4)
#     list = pool.map(getHashTags, postCrawl(parse(crawl())))
#     for i in list:
#         print(i)

# getHashTags(postCrawl(parse(crawl())))
