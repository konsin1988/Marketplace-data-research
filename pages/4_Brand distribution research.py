import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from streamlit_data.get_data import load_session_state
load_session_state()

from streamlit_funcs.brand_compare import BrandCompare

st.header('Brand distribution research')
st.text('In this chapter, our goal is to examine the distribution of brands that are found in all three marketplaces, looking at their relative number (as a percentage of the total number of brands in the category).')
st.text('Percentages and graphs can be viewed for each product category.')
search_var = st.sidebar.radio('Search query', st.session_state.search_query_list)

brandCompare = BrandCompare()
brandCompare.init_compare_dataframes(search_var)

for col, mp_name in zip(st.columns([0.33, 0.33, 0.33]), ['Lamoda', 'Wildberries', 'Ozon']):
    brandCompare.df_st_printer(col, mp_name)

st.plotly_chart(brandCompare.plotter_compare())
    
st.success("As we can see from the graphs, the distribution of brands in percentage terms differs across marketplaces. Those brands that are represented in large quantities in one marketplace may have a minimal number in another.")

st.subheader('Single brand distribution')
st.text("Now let's look at the ratio of brands represented in all three marketplaces and all the others.")
brandCompare.plotter_single()
st.success(r"""The graphs allow us to draw the following conclusions:
1) The most popular brands presented in all three marketplaces are not always the most popular in a particular marketplace.
2) The largest number of popular brands for all three marketplaces are in Ozon, in most cases, brands that are popular and presented in all three marketplaces also occupy leading positions in Ozon.""")

if st.checkbox('Show code snippets', value=False):
    brandCompare.code_printer()