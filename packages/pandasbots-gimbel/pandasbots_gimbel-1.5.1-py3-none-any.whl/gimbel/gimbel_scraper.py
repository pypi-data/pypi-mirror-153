'''
# Project Gimbel Mexicana
* Author: Rafael Klanfer Nunes
* Date: 30/05/2022
'''

import json
import logging
# PACKAGES
import re

import pandas as pd
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# FUNCTIONS

class Webscrap():
    """
    Class Webscrap. Will create a driver to scrap the url and return data from the website.
    """
    # Initialize variables
    def __init__(self, url) -> None:
        self.url = url
        self.id = url.split("/")[-1]
    # Return of the object Webscrap
    def __str__(self) -> str:
        return f"The url is: {self.url}"

    def create_driver(self):
        # 1. Driver Options
        options = webdriver.ChromeOptions()
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_argument("window-size=1280,800")
        options.add_argument("user-agent=Chrome/74.0.3729.169")
        options.headless = True
        options.add_argument("user-data-dir=selenium")
        # 2. Create Driver
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        return driver
    
    def open_url(self, driver) -> None:
        # 1. Open URL
        driver.get(self.url)
        return None

    def close_driver(self, driver) -> None:
        # 1. Close Driver
        driver.quit()
        return None
    
    def get_html(self, driver) -> str:
        # 1. Get the page source
        html = driver.page_source
        return html

    def create_df(self, html) -> pd.DataFrame:
        soup = bs(html, features="html.parser")
        header = []
        linha = []
        table = soup.find('table', attrs={'class':'table table-striped w-auto r_corners wraper shadow t_xs_align_c border-bottom-brand'})
        table_body = table.find('tbody')
        rows = table_body.find_all('tr')
        for row in rows:
            cols = row.find_all('th')
            cols = [ele.text.strip() for ele in cols]
            header.append([ele for ele in cols if ele]) # Get rid of empty values
            lins = row.find_all('td')
            lins = [ele1.text.strip() for ele1 in lins]
            linha.append([ele1 for ele1 in lins if ele1]) # Get rid of empty values
        df = pd.DataFrame(linha, columns=header[0])
        df.to_excel(f"info_product_{self.id}.xlsx")
        return df

    def get_images(self, html):
        list_images = []
        regex = r"src=\"\/gimbel\/img\/products_images\/thumb\/(.*?)\" title"

        matches = re.finditer(regex, html, re.MULTILINE)

        for match in matches:
            list_images.append(f"https://gimbelmexicana.com/gimbel/img/products_images/thumb/{match.group(1)}")

        # Make a list of unique values
        set_images  = set(list_images)

        return set_images


    def get_info(self) -> dict:
        # 1. Create driver
        driver = self.create_driver()
        # 2. Open URL
        self.open_url(driver)
        # wait
        driver.implicitly_wait(2)
        # Get html of url
        html = self.get_html(driver)
        # 1. Find Element
        # 1.1. BRAND
        xpath_brand = "/html/body/div[1]/div[2]/div/div[1]/a[1]"
        brand = driver.find_element(By.XPATH, xpath_brand).text
        # 1.2. CODE
        xpath_code = "/html/body/div[1]/div[2]/div/div[2]/div/div/div[2]/div[1]/h5"
        code = driver.find_element(By.XPATH, xpath_code).text
        # 1.3. NAME
        xpath_name = "/html/body/div[1]/div[2]/div/div[2]/div/div/div[2]/div[1]/h4"
        name = driver.find_element(By.XPATH, xpath_name).text
        # 1.4. DETAILS
        id_details = "plcRoot_Layout_znProducto_ProductoQV_userControlElem_lblDescripcion"
        details = driver.find_element(By.ID, id_details).text
        # 1.5. INFO
        df_info = self.create_df(html)
        ## Assign as json to export later
        df_info_json = df_info.to_json()
        # 1.6. IMAGES
        set_images = self.get_images(html)
        ### Asing as list to be serialized later
        list_images = list(set_images)
        # 1.7. Create object JSON to return
        response_json = {"Brand": brand,
                        "Code": code,
                        "Name": name,
                        "Details": details,
                        "Info": df_info_json,
                        "Image": list_images}
        driver.implicitly_wait(2)
        # 4. Close Driver
        self.close_driver(driver)
        return response_json

    # Save JSON to file
    def save_data(self, response_json) -> None:
        with open(f"data_product_{self.id}.json", "w") as f:
            json.dump(response_json, f, indent=4, ensure_ascii=False)
        return None
        
    # Open Json File with product data.
    def open_data(self) -> dict:
        with open(f"data_product_{self.id}.json", "r") as f:
            response_json = json.load(f)
        return response_json

# Main Function
def get_product_info(url):
    ''''
    Function to get the product info from the url.
    '''
    logging.info("\n##### SYSTEM START #####\n")
    logging.info("\nSystem running, please wait....")
    # Create object
    product = Webscrap(url)
    # Get product info
    product_info = product.get_info()
    # Save product info
    product.save_data(product_info)
    logging.info("\n##### SYSTEM END #####\n")
    # Return product info
    return product_info
