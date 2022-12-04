from typing_extensions import runtime
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

URL = "http://orteil.dashnet.org/experiments/cookie/"
TIME_RUN = 1
WAITTIME = 10
CHROMEDRIVER_PATH = "C:\Development\chromedriver.exe"

service = Service(CHROMEDRIVER_PATH)
driver = webdriver.Chrome(service=service)
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
 

def clickCookie():
    cookie = driver.find_element(By.ID, "cookie")
    cookie.click()


driver.get(URL)


#Get upgrade item ids.
items = driver.find_elements(By.CSS_SELECTOR, "#store div")
item_ids = [item.get_attribute("id") for item in items]

timeout = time.time() + WAITTIME
runtime = time.time() + (60 * TIME_RUN) 

while True:
    clickCookie()

    if time.time() > timeout:

        #Get all upgrade <b> tags
        all_prices = driver.find_elements(By.CSS_SELECTOR, "#store b")
        item_prices = []

        #Convert <b> text into an integer price.
        for price in all_prices:
            element_text = price.text
            if element_text != "":
                cost = int(element_text.split("-")[1].strip().replace(",", ""))
                item_prices.append(cost)

        #Create dictionary of store items and prices
        cookie_upgrades = {}
        for n in range(len(item_prices)):
            cookie_upgrades[item_prices[n]] = item_ids[n]

        #Get current cookie count
        money_element = driver.find_element(By.ID, "money").text
        if "," in money_element:
            money_element = money_element.replace(",", "")
        cookie_count = int(money_element)

        #Find upgrades that we can currently afford
        affordable_upgrades = {}
        for cost, id in cookie_upgrades.items():
            if cookie_count > cost:
                 affordable_upgrades[cost] = id

        #Purchase the most expensive affordable upgrade
        highest_price_affordable_upgrade = max(affordable_upgrades)
        print(highest_price_affordable_upgrade)
        to_purchase_id = affordable_upgrades[highest_price_affordable_upgrade]

        driver.find_element(By.ID, to_purchase_id).click()
        
        timeout = time.time() + WAITTIME
        

    if time.time() > runtime:
        cookie_per_s = driver.find_element(By.ID, "cps").text
        print(cookie_per_s)
        break
