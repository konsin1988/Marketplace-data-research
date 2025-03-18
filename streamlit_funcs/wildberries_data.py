import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from fake_useragent import UserAgent

import re
from bs4 import BeautifulSoup
import pandas as pd

def get_one_page(service, page_num, search_query, gender, start_price, end_price):
    digits = re.compile(r'[0-9]*')
    gender_number = {
        'Men': 1,
        'Women': 2,
        'Kids': 3
    }
    brands = []
    product_names = []
    prices = []

    options = ChromeOptions()
    ua = UserAgent()
    user_agent = ua.random
    options.add_experimental_option("excludeSwitches", ["enable-automation"])  
    options.add_experimental_option('useAutomationExtension', False) 
    options.add_argument('--headless')
    options.add_argument("--disable-extensions")
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    options.add_argument(f"--user-agent={user_agent}")
    options.add_argument(f'--remote-debugging-port={9222+page_num}')

    try:
        driver.quit()
    except:
        pass
    driver = webdriver.Chrome(service=service, options=options)
    driver.get(f"https://www.wildberries.ru/catalog/0/search.aspx?page={page_num + 1}&sort=popular&search={search_query}&priceU={start_price}00%3B{end_price}00&fkind={gender_number[gender]}")
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'product-card__middle-wrap')))
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        content = soup.find('div', class_='product-card-overflow')
        product_cards = content.find_all('div', class_='product-card__middle-wrap')
        for card in product_cards:
            brand = card.find('h2', class_='product-card__brand-wrap').text
            product_names.append(brand.split('/')[1].strip())
            brands.append(brand.split('/')[0].strip())
            prices.append(re.search(digits, ''.join(card.text.split('₽')[0].split()))[0])
    except Exception as e:
        print(f'Error: {e}')  
        driver.quit()
    finally:
        driver.quit()
        
    
    result = pd.DataFrame({'Brand': brands, 'ProductName': product_names, 'Price': prices})
    return result

def wildberries_parsing(service, search_query, gender, price_levels):
    st.dataframe(get_one_page(service, 0, search_query, gender, price_levels[0], price_levels[1]))

def wildberries_print_code():
    st.code(r"""
import streamlit as st
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from fake_useragent import UserAgent

import re
from bs4 import BeautifulSoup
import pandas as pd

def get_one_page(service, page_num, search_query, gender, start_price, end_price):
    digits = re.compile(r'[0-9]*')
    gender_number = {
        'Men': 1,
        'Women': 2,
        'Kids': 3
    }
    brands = []
    product_names = []
    prices = []

    options = ChromeOptions()
    ua = UserAgent()
    user_agent = ua.random
    options.add_experimental_option("excludeSwitches", ["enable-automation"])  
    options.add_experimental_option('useAutomationExtension', False) 
    options.add_argument('--headless')
    options.add_argument("--disable-extensions")
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    options.add_argument(f"--user-agent={user_agent}")
    options.add_argument(f'--remote-debugging-port={9222+page_num}')

    driver = webdriver.Chrome(service=service, options=options)
    driver.get(f"https://www.wildberries.ru/catalog/0/search.aspx?page={page_num + 1}&sort=popular&search={search_query}&priceU={start_price}00%3B{end_price}00&fkind={gender_number[gender]}")
    try:
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'product-card__middle-wrap')))
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        content = soup.find('div', class_='product-card-overflow')
        product_cards = content.find_all('div', class_='product-card__middle-wrap')
        for card in product_cards:
            brand = card.find('h2', class_='product-card__brand-wrap').text
            product_names.append(brand.split('/')[1].strip())
            brands.append(brand.split('/')[0].strip())
            prices.append(re.search(digits, ''.join(card.text.split('₽')[0].split()))[0])
    except Exception as e:
        print(f'Error: {e}')  
    finally:
        driver.quit()
        
    
    result = pd.DataFrame({'Brand': brands, 'ProductName': product_names, 'Price': prices})
""", 'python')

if __name__ == 'main':
    wildberries_parsing