from selenium import webdriver

chrome_path = r"/Users/joyp.isahac/Downloads/chromedriver"

browser = webdriver.Chrome(chrome_path)

browser.get('http://localhost:8000')

assert 'Django' in browser.title