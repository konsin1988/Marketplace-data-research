import streamlit as st
from selenium.webdriver.chrome.service import Service
import pandas as pd

def load_session_state():
    st.set_page_config(
        # layout="wide", 
        page_title='Marketplace data research', 
        page_icon="🏪"
        )
    
    if 'price_levels' not in st.session_state:
        st.session_state.price_levels = (None, None)

    if 'search_query' not in st.session_state:
        st.session_state.search_query = None

    if 'marketplace' not in st.session_state:
        st.session_state.marketplace = None

    if 'gender' not in st.session_state:
        st.session_state.gender = None
    
    if 'service' not in st.session_state:
        st.session_state.service = None

    if 'search_query_list' not in st.session_state:
        st.session_state.search_query_list = ['Брюки', 'Рубашка', 'Джинсы', 'Свитшот', 'Худи', 'Шорты']

    if 'mp_names' not in st.session_state:
        st.session_state.mp_names = ['Lamoda', 'Wildberries', 'Ozon']

    if 'marketplaces' not in st.session_state:
        st.session_state.marketplaces = {
            'Lamoda': pd.read_csv('marketplace_data/lamoda_03.2025.csv'),
            'Wildberries': pd.read_csv('marketplace_data/wb_03.2025.csv'),
            'Ozon': pd.read_csv('marketplace_data/ozon_03.2025.csv')
        }