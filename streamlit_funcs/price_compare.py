import streamlit as st
from plotly._subplots import make_subplots
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

class PriceCompare():
    def __query_filter_df(self, df):
        return (
            df.query(f'SearchQuery == "{self.__query}"')
        )
    
    def init_dataframes(self, query):
        self.__query = query
        self.__dfs = {nm_name: self.__query_filter_df(df) for nm_name, df in st.session_state.marketplaces.items()}

    def plot_boxes(self):

        fig = make_subplots(rows=1, cols=3, shared_yaxes=True)
        for i, mp_name in enumerate(st.session_state.mp_names):
            df_query = self.__dfs[mp_name].query("Price <= 15000")
            fig.add_trace(
                go.Box(
                    y = df_query['Price'],
                    name=mp_name,
                    line_color=px.colors.qualitative.Pastel1[i],
                    fillcolor=None
                    ),
                col = i+1, row = 1
            )
        fig.add_hline(
            y = self.__dfs['Wildberries']['Price'].median(),
            line_dash="dot", row=1, col=1, line_color="red", line_width=2
            )
        fig.add_hline(
            y = self.__dfs['Ozon']['Price'].median(),
            line_dash="dot", row=1, col=1, line_color="blue", line_width=2
            )
        fig.update_layout(
            title_text = 'Distribution of price over marketplaces and product types'
        )

        st.plotly_chart(fig)

    def plot_mean_bar(self):
        means_list = []
        for i, mp_name in enumerate(st.session_state.mp_names):
            means_list.append(self.__dfs[mp_name]['Price'].mean().round(2))
        df = pd.DataFrame({'Marketplace': st.session_state.mp_names, 'Mean price': means_list})
        fig = px.bar(
            df,
            x = 'Marketplace',
            y = 'Mean price',
            title = 'Mean absolute price',
            text='Mean price'
        )
        st.plotly_chart(fig)
        

        fig = px.bar(
            df.assign(Mean_perc = lambda x: (x['Mean price'] * 100 / x['Mean price'].sum()).round(2)),
            x = 'Marketplace',
            y = 'Mean_perc',
            title = 'Percent of sum mean prices',
            labels={
                'Mean_perc': 'Percent of sum mean prices'
            },
            text='Mean_perc'
        )
        st.plotly_chart(fig)

    def plot_gender_dif(self):
        for mp_name in st.session_state.mp_names:
            fig = px.box(
                (
                    self.__dfs[mp_name]
                    .assign(Gender = lambda x: x['Gender'].map(lambda x: x.capitalize()))
                    # .assign(std)
                    .query("Price < 3 * Price.std()")
                ),
                y = 'Price',
                color='Gender',
                title=f'Price distribution over gender on {mp_name}',
                x = 'Gender'
            )

            st.plotly_chart(fig)
            

if __name__ == 'main':
    PriceCompare()