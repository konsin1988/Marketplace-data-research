import streamlit as st
import pandas as pd
from bs4 import BeautifulSoup
import re

from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from concurrent.futures import ThreadPoolExecutor, as_completed

from fake_useragent import UserAgent
from selenium_stealth import stealth

from time import sleep

# 125165 - women
# 125166 - men
# 135513 - kids

def ozon_parsing(service, search_query, gender, price_levels):

    options = ChromeOptions()
    ua = UserAgent()
    user_agent = ua.random
    options.add_experimental_option("excludeSwitches", ["enable-automation"])    # stealth
    options.add_experimental_option('useAutomationExtension', False) 
    options.add_argument('--headless')
    options.add_argument("--disable-extensions")
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    options.add_argument(f"--user-agent={user_agent}")
    # options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36")
    options.add_argument(f'--remote-debugging-port={9222}')
    
    gender_dict = {
        'Men': 125166,
        'Women': 125165,
        'Kids': '135533%2C135532'
    }
    prices = []
    brands = []
    product_names = []
    
    
    try: 
        driver.quit()
        sleep(1)
    except:
        pass
    driver = webdriver.Chrome(service=service, options=options)
    
    stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
            )
    driver.get(f"https://www.ozon.ru/category/odezhda-obuv-i-aksessuary-7500/?category_was_predicted=true&currency_price={price_levels[0]}.000%3B{price_levels[1]}.000&deny_category_prediction=true&from_global=true&sexmaster={gender_dict[gender]}&text={search_query}")
    sleep(1)
    try:
        WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.ID, 'paginator')))
        # for _ in range(5):
        #     driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        #     sleep(1)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        content = soup.find('div', id='paginator')
        product_name_span = content.find_all('span', class_='tsBody500Medium')
        for product_name in product_name_span:
            product_names.append(product_name.text)
        brands_list = content.find_all('div', class_='m1j_25')
        for brand in brands_list:
            prices.append(''.join(brand.text.split()).split('₽')[0])
            match = re.search(r"""((?<=\s)|(?<=[Ё-ё])|(?<=%))[A-Za-z]+?((\s|'|\.)[A-Za-z]+?){0,1}((?=\s)|(?=[Ё-ё0-9]))""", brand.text)
            if match:
                brands.append(match[0])
            else:
                match = re.search(r"""[А-ЯЁ]{3,}""", brand.text)
                if match:
                    brands.append(match[0])
                else:
                    brands.append(None)
      
    except Exception as e:
        print(f'Error: {e}')
        driver.quit()
    finally:
        driver.quit()

    result = pd.DataFrame({'Brand': brands, 'ProductName': product_names, 'Price': prices})
    st.dataframe(result)

def ozon_print_code():
    st.code(r'''
import streamlit as st
import pandas as pd
from bs4 import BeautifulSoup
import re

from selenium import webdriver
from selenium.webdriver import ChromeOptions
from selenium.webdriver.common.by import By

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from concurrent.futures import ThreadPoolExecutor, as_completed

from fake_useragent import UserAgent
from selenium_stealth import stealth

from time import sleep
            
def ozon_parsing(service, search_query, gender, price_levels):

    options = ChromeOptions()
    ua = UserAgent()
    user_agent = ua.random
    options.add_experimental_option("excludeSwitches", ["enable-automation"])    # stealth
    options.add_experimental_option('useAutomationExtension', False) 
    options.add_argument('--headless')
    options.add_argument("--disable-extensions")
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--no-sandbox')
    options.add_argument(f"--user-agent={user_agent}")
    options.add_argument(f'--remote-debugging-port={9222}')
    
    gender_dict = {
        'Men': 125166,
        'Women': 125165,
        'Kids': '135533%2C135532'
    }
    prices = []
    brands = []
    product_names = []
    
    driver = webdriver.Chrome(service=service, options=options)
    stealth(driver,
            languages=["en-US", "en"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
            )
    driver.get(f"https://www.ozon.ru/category/odezhda-obuv-i-aksessuary-7500/?category_was_predicted=true&currency_price={price_levels[0]}.000%3B{price_levels[1]}.000&deny_category_prediction=true&from_global=true&sexmaster={gender_dict[gender]}&text={search_query}")
    try:
        WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.ID, 'paginator')))
        for _ in range(5):
            driver.execute_script('window.scrollTo(0, document.body.scrollHeight);')
            sleep(1)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        content = soup.find('div', id='paginator')
        product_name_span = content.find_all('span', class_='tsBody500Medium')
        for product_name in product_name_span:
            product_names.append(product_name.text)
        brands_list = content.find_all('div', class_='m1j_25')
        for brand in brands_list:
            prices.append(''.join(brand.text.split()).split('₽')[0])
            match = re.search(r"""((?<=\s)|(?<=[Ё-ё])|(?<=%))[A-Za-z]+?((\s|'|\.)[A-Za-z]+?){0,1}((?=\s)|(?=[Ё-ё0-9]))""", brand.text)
            if match:
                brands.append(match[0])
            else:
                match = re.search(r"""[А-ЯЁ]{3,}""", brand.text)
                if match:
                    brands.append(match[0])
                else:
                    brands.append(None)
      
    except Exception as e:
        print(f'Error: {e}')
    finally:
        driver.quit()

    result = pd.DataFrame({'Brand': brands, 'ProductName': product_names, 'Price': prices})
''', 'python')