import streamlit as st

from selenium.webdriver.chrome.service import Service

from streamlit_data.get_data import load_session_state
from streamlit_funcs.lamoda_data import lamoda_parsing, lamoda_print_code
from streamlit_funcs.wildberries_data import wildberries_parsing, wildberries_print_code
from streamlit_funcs.ozon_data import ozon_parsing, ozon_print_code

load_session_state()
st.session_state.service = Service()

st.header('Realtime web scraping')
st.text('Data that we get due to realtime scraping not anouth to do some research. I have parsed the data for further analysis in the past.')

st.info("Since we are dealing with large sites that are in constant change, there is a possibility that by the time you view this work, some parts of the code will no longer give an error. This is possible, that's life. That's why I am attaching the source code, which you can take and correct if you wish.")

col_market, col_type = st.columns([0.5, 0.5])

st.session_state.marketplace = col_market.selectbox('Marketplace', 
                                                    ('Lamoda', 'Wildberries', 'Ozon'))

st.session_state.search_query = col_type.selectbox('Product type', 
                                  ('Брюки', 'Рубашка', 'Джинсы', 'Свитшот', 'Худи', 'Шорты'), 
                                  index=0)


col_gender, col_slide = st.columns([0.5, 0.5])

st.session_state.gender = col_gender.selectbox('Gender', ('Men', 'Women', 'Kids'))

st.session_state.price_levels = col_slide.slider('Price option', 0, 50000, (0, 50000))



if st.session_state.marketplace == 'Lamoda':
    if st.checkbox('Show code snippets',value=False):
        lamoda_print_code()
    lamoda_parsing(st.session_state.search_query,
                            st.session_state.gender,
                            st.session_state.price_levels
                            )
elif st.session_state.marketplace == 'Wildberries':
    if st.checkbox('Show code snippets', value = False):
        wildberries_print_code()
    wildberries_parsing(st.session_state.service,
                        st.session_state.search_query,
                        st.session_state.gender,
                        st.session_state.price_levels)

elif st.session_state.marketplace == 'Ozon':
    if st.checkbox('Show code snippets', value=False):
        ozon_print_code()
    ozon_parsing(st.session_state.service,
                 st.session_state.search_query,
                 st.session_state.gender,
                 st.session_state.price_levels) 
    