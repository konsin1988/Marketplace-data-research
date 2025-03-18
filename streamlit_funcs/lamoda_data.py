import streamlit as st
import pandas as pd
from bs4 import BeautifulSoup
import requests as rq
import re
from concurrent.futures import ThreadPoolExecutor

def pars_one_page(page_num, search_query, gender, start_price, end_price):
    gender_dict = {
    'Men': 'men',
    'Women': 'women',
    'Kids': 'kids'
    }
    brands = []
    product_names = []
    prices = []
    response = rq.get(rf'''https://www.lamoda.ru/catalogsearch/result/?q="{search_query}"&submit=y&gender_section={gender_dict[gender]}&price={start_price},{end_price}&page={page_num+1}''')
    try:
        soup = BeautifulSoup(response.text, 'html.parser')
        content = soup.find('div', class_='grid__catalog')
        product_cards = content.find_all('div', class_='x-product-card-description')
        for card in product_cards:
            brands.append(card.find('div', class_='x-product-card-description__brand-name').text.strip())
            product_names.append(card.find('div', class_='x-product-card-description__product-name').text.strip())
            prices.append(int(card.find_all('span', class_=re.compile(r'x-product-card-description__price-[a-z]*?(?=(\b)|("))'))[-1]
                .text
                .strip()
                .replace(' ', '')
                .replace('₽', ''))
                )
    
    except Exception as e:
        print(f'Error: {e}')
    result = pd.DataFrame({'Brand': brands, 'ProductName': product_names, 'Price': prices})
    return result


def lamoda_parsing(search_query, gender, price_levels):
    page_nums = [i for i in range(20)]
    with ThreadPoolExecutor(max_workers=8) as executor:
        result = list(executor.map(lambda page_num: pars_one_page(page_num, search_query, gender, price_levels[0], price_levels[1]), page_nums))
    st.dataframe(pd.concat(result).reset_index(drop=True))
    

def lamoda_print_code():
    st.code(r"""
import streamlit as st
import pandas as pd
from bs4 import BeautifulSoup
import requests as rq
import re
from concurrent.futures import ThreadPoolExecutor

def pars_one_page(page_num, search_query, gender, start_price, end_price):
    gender_dict = {
    'Men': 'men',
    'Women': 'women',
    'Kids': 'kids'
    }
    brands = []
    product_names = []
    prices = []
    response = rq.get(rf'''https://www.lamoda.ru/catalogsearch/result/?q="{search_query}"&submit=y&gender_section={gender_dict[gender]}&price={start_price},{end_price}&page={page_num+1}''')
    try:
        soup = BeautifulSoup(response.text, 'html.parser')
        content = soup.find('div', class_='grid__catalog')
        product_cards = content.find_all('div', class_='x-product-card-description')
        for card in product_cards:
            brands.append(card.find('div', class_='x-product-card-description__brand-name').text.strip())
            product_names.append(card.find('div', class_='x-product-card-description__product-name').text.strip())
            prices.append(int(card.find_all('span', class_=re.compile(r'x-product-card-description__price-[a-z]*?(?=(\b)|("))'))[-1]
                .text
                .strip()
                .replace(' ', '')
                .replace('₽', ''))
                )
    
    except Exception as e:
        print(f'Error: {e}')
    result = pd.DataFrame({'Brand': brands, 'ProductName': product_names, 'Price': prices})
    return result


def lamoda_parsing(search_query, gender, price_levels):
    page_nums = [i for i in range(20)]
    with ThreadPoolExecutor(max_workers=8) as executor:
        result = list(executor.map(lambda page_num: pars_one_page(page_num, search_query, gender, price_levels[0], price_levels[1]), page_nums))
    st.dataframe(pd.concat(result).reset_index(drop=True))
""", 'python')

if __name__ == 'main':
    lamoda_parsing, lamoda_print_code