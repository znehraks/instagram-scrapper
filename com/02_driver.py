from selenium import webdriver

driver = webdriver.Chrome(
    executable_path="../webdriver/chromedriver.exe"
)

url = "https://www.instagram.com/explore/tags/%ED%99%8D%EC%B0%A8/?hl=ko"
driver.get(url)
driver.close()
