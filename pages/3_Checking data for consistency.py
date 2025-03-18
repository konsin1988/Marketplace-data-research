import streamlit as st
import pandas as pd
import io
import plotly.express as px

from streamlit_data.get_data import load_session_state
load_session_state()

from streamlit_funcs.get_overview import get_overview

st.header('Checking data for consistency')
mp_var = st.sidebar.radio('Marketplace', ('Lamoda', 'Wildberries', 'Ozon'))
pt_var = st.sidebar.radio('Search query', st.session_state.search_query_list)
get_overview(mp_var, pt_var)