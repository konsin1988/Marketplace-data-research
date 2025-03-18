import streamlit as st

from streamlit_data.get_data import load_session_state
load_session_state()

from streamlit_funcs.price_compare import PriceCompare
priceCompare = PriceCompare()


st.header("Price distribution over groups")
search_query = st.sidebar.radio('Search query', st.session_state.search_query_list)

priceCompare.init_dataframes(search_query)

priceCompare.plot_boxes()
st.success('As we can see from the graphs, the median price on Lamoda for all types of goods is significantly higher than on the other two marketplaces. Differences between Wildberries and Ozon, if any, are extremely insignificant. Median prices on Wildberries are always slightly higher, while Ozon has a very large number of outliers.')

priceCompare.plot_mean_bar()
st.success('The average price of goods on Lamoda is on average three times higher than on other trading platforms.')

st.subheader('Gender price difference')
st.text("Let's look at the price difference between men's, women's and children's products on different marketplaces.")
st.info("For clarity of the graphs, I have removed prices that exceed 3 standard deviations.")

priceCompare.plot_gender_dif()
st.success("The graphs show that, unlike other marketplaces, on Lamoda, prices for children's clothing are approximately equal to prices for adults. Prices for men's and women's clothing do not differ significantly on any marketplace; women's clothing can be purchased slightly cheaper on Ozon.")