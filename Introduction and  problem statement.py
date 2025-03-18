import streamlit as st
from selenium.webdriver.chrome.service import Service
from streamlit_data.get_data import load_session_state

load_session_state()
st.session_state.service = Service()

st.title('Comparative analysis of prices on popular online trading platforms')

st.text("Working with data is the main part of a data analyst's work. But it is not always possible to simply take this data from a resource; sometimes it is necessary to make an effort (and sometimes considerable) to obtain the information that is needed. This is what we will do in this work.")
st.info("I would like to point out right away that according to the law of the Russian Federation, parsing is a violation only in the case of obtaining financial benefit through the obtained data. In our case, this is just research.")
st.subheader('Statement of the problem')
st.text('Our research will focus exclusively on clothing sales, or more precisely, we will take 6 types.')
st.markdown("### In our work we set the following goals:")
st.markdown(r"""
- Understand how each of the sites from which we plan to obtain information works: its features, its CSS classes, how access to the next page is provided (if there is one)
- Write two types of scrapers: for parsing a large amount of information and for parsing a small amount in real time
- Pre-process the received information: check for duplicates, missing data (this is especially true for the ozon website, where the work turned out to be the most difficult)
- Conduct a general analysis of the variables, look at the distributions, check for outliers
- Form assumptions and hypotheses
- Confirm these hypotheses graphically or analytically
""")
st.info(r'''I will say that I did not filter prices by ascending/descending order during the scraping process. The main idea was to analyze the prices of goods that marketplaces offer "out of the box". To understand what level of material support each site is focused on, what it offers as "popular" for its customers.''')

st.text("The idea to take these marketplaces in particular is due to their enormous popularity, particularly in the clothing retail sector.")
st.image("https://s.rbk.ru/v5_marketing_media/resized/1180x730/images/7/89/115959358679897.jpg")
st.markdown('*The image was taken from the site https://marketing.rbc.ru/*')