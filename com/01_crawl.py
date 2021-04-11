from libs.crawler import crawl

url = "https://www.instagram.com/explore/tags/%ED%99%8D%EC%B0%A8/?hl=ko"

pageString = crawl(url)
print(pageString)
