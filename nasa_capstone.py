import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import json
import csv
from datetime import datetime

chrome_options = Options()
chrome_options.add_argument("--headless")
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--window-size=1920x1080")
chrome_options.add_argument("start-maximised")
options = webdriver.ChromeOptions()
options.add_experimental_option('detach', True)
options.add_experimental_option('excludeSwitches', ['enable-logging'])

class Web_Crawler:

    def __init__(self):
        ######## INITIALISE WEB DRIVER ######## 
        self.driver = webdriver.Chrome(options=chrome_options)
        self.url = 'https://mars.nasa.gov/msl/mission/weather/'
        self.row_data = []


    def scrape_data(self) -> webdriver.Chrome:
        ######## SCRAPE THE CURIOSITY PAGE FOR WEATHER DATA ########
        self.url = 'https://mars.nasa.gov/msl/mission/weather/'
        self.driver.get(self.url)
        time.sleep(3)
        data = self.driver.find_elements(By.XPATH, value='//*[@id="weather_observation"]/tbody')
        for i in data:
            self.row_data.append(i.text)
        test = self.row_data
        self.row_data = test[0].split('\n')
        time.sleep(1)
        self.export_csv()

    def export_csv(self):
        ######## FORMAT AND EXPORT DATA TO CSV FORMAT ########
        formatted_data = []
        for row in self.row_data:
            row_parts = row.split()
            date_str = ' '.join(row_parts[:3])
            date_obj = datetime.strptime(date_str, "%B %d, %Y")
            formatted_date = date_obj.strftime("%Y-%m-%d")
            temperature_max = row_parts[4].replace(',', '')
            temperature_min = row_parts[5].replace(',', '')
            formatted_data.append([formatted_date, row_parts[3], temperature_max, temperature_min, row_parts[6], row_parts[7], row_parts[8]])

        with open('mars.csv', 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["Date", "Sol Number", "Temperature Max", "Temperature Min", "Pressure", "Sunrise", "Sunset"])
            writer.writerows(formatted_data)



init_crawling = Web_Crawler()
init_crawling.scrape_data()