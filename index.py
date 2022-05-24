import time
import csv
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
url = "https://en.wikipedia.org/wiki/List_of_brightest_stars_and_other_record_stars"
browser = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
browser.get(url)
time.sleep(3)
stars = []

def scrape():
    soup = BeautifulSoup(browser.page_source, "html.parser")
    startable = soup.find("table").find("tbody")
    table_rows = startable.find_all("tr")
    for i, tr in enumerate(table_rows):
        temp = []
        td = tr.find_all("td")
        if td[1].find("a") != None: temp.append(td[1].find("a").contents[0])
        else: temp.append(td[1].contents[0])
        temp.append(browser.find_element_by_xpath(f'//*[@id="mw-content-text"]/div[1]/table/tbody/tr[{i+1}]/td[4]').text)
        mass = td[5].contents[0].strip().replace('"', "", 2)
        radius = td[6].contents[0].strip().replace('"', "", 2)
        temp.append(mass)
        temp.append(radius)
        stars.append(temp)

scrape()
headers = ["name", "distance", "mass", "radius"]
with open("stars.csv", "w") as f:
    cw = csv.writer(f)
    cw.writerow(headers)
    for i in stars:
        print(i)
        cw.writerow(i)