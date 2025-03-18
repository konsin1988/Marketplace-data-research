import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px

class BrandCompare():
    def __get_brand_intersection(self, df1, df2, df3):
        return (
            list(set(df1['Brand'].str.lower()) & set(df2['Brand'].str.lower()) & set(df3['Brand'].str.lower()))
        )
    
    def __get_brands_df(self, df, search_query):
        return (
            df
            .query(f'SearchQuery == "{search_query}"')
            ['Brand'].str.lower()
            .value_counts()
            .reset_index()
            .assign(Percent = lambda x: (x['count'] * 100 / x['count'].sum()).round(2))
            [['Brand', 'Percent']]
        )
    
    def __df_filtering(self, df, list_intersection):
        return df.query(f"(Brand.str.lower() in {list_intersection})").reset_index(drop=True)
    
    def __get_merged(self):
        return (
            self.__lamoda_brands_gen
            .set_index('Brand')
            .merge(self.__wb_brands_gen.set_index('Brand'), on='Brand')
            .merge(self.__ozon_brands_gen.set_index('Brand'), on='Brand')
            .rename({'Percent_x': 'Lamoda', 'Percent_y': 'Wildberries', 'Percent': 'Ozon'}, axis = 1)
            .reset_index()
        )
    
    def __plot_bar(self, fig, df, mp_name):
        fig.add_bar(
            x = df['Brand'],
            y = df[mp_name],
            name=mp_name
        )
        return fig

    def init_compare_dataframes(self, query):
        self.__query = query
        lamoda_brands = self.__get_brands_df(st.session_state.marketplaces['Lamoda'], query)
        wb_brands = self.__get_brands_df(st.session_state.marketplaces['Wildberries'], query)
        ozon_brands = self.__get_brands_df(st.session_state.marketplaces['Ozon'], query)
        self.__brand_intersection = self.__get_brand_intersection(lamoda_brands, wb_brands, ozon_brands)

        self.__lamoda_brands_gen = self.__df_filtering(lamoda_brands, self.__brand_intersection)
        self.__wb_brands_gen = self.__df_filtering(wb_brands, self.__brand_intersection)
        self.__ozon_brands_gen = self.__df_filtering(ozon_brands, self.__brand_intersection)
    
    def __set_category(self, df):
        return (
            df
            .assign(is_general = lambda x: x['Brand']
            .str.lower().map(lambda x: 'General' if x in self.__brand_intersection else 'Not in all MP'))
        )

    def __get_labeled_brands(self):
        lamoda_brands = self.__get_brands_df(st.session_state.lamoda_df, self.__query)
        wb_brands = self.__get_brands_df(st.session_state.wb_df, self.__query)
        ozon_brands = self.__get_brands_df(st.session_state.ozon_df, self.__query)

        return {'Lamoda': self.__set_category(lamoda_brands), 
                'Wildberries': self.__set_category(wb_brands), 
                'Ozon': self.__set_category(ozon_brands)}

    def df_st_printer(self, col, mp_name):
        col.markdown(f'#### {mp_name}')
        col.dataframe(self.__get_merged().set_index('Brand')[[mp_name]].sort_values(mp_name, ascending = False))

    def plotter_compare(self):
        fig = go.Figure()
        for mp_name in st.session_state.mp_names:
            fig = self.__plot_bar(fig, self.__get_merged(), mp_name)
        return fig
    
    def plotter_single(self):
        dfs = self.__get_labeled_brands()
        for mp_name in st.session_state.mp_names:
            df = dfs[mp_name].iloc[:30, :] 
            fig = px.bar(
                df,
                x = 'Brand',
                y = 'Percent',
                color = 'is_general',
                labels={
                    'is_general': 'Is general to all MP'
                },
                category_orders={
                    'Brand': df['Brand'],
                    'is_general': ['General', 'Not in all MP']
                },
                color_discrete_sequence=px.colors.qualitative.Dark24,
            )
            fig.update_layout(
                title = dict(
                    text = mp_name,
                    font = dict(
                        size = 20,
                        weight = 'bold'
                    )
                )
            )
            st.plotly_chart(fig)
            
    
    def code_printer(self):
        st.code(r'''
class BrandCompare():
    def __get_brand_intersection(self, df1, df2, df3):
        return (
            list(set(df1['Brand'].str.lower()) & set(df2['Brand'].str.lower()) & set(df3['Brand'].str.lower()))
        )
    
    def __get_brands_df(self, df, search_query):
        return (
            df
            .query(f'SearchQuery == "{search_query}"')
            ['Brand'].str.lower()
            .value_counts()
            .reset_index()
            .assign(Percent = lambda x: (x['count'] * 100 / x['count'].sum()).round(2))
            [['Brand', 'Percent']]
        )
    
    def __df_filtering(self, df, list_intersection):
        return df.query(f"(Brand.str.lower() in {list_intersection})").reset_index(drop=True)
    
    def __get_merged(self):
        return (
            self.__lamoda_brands_gen
            .set_index('Brand')
            .merge(self.__wb_brands_gen.set_index('Brand'), on='Brand')
            .merge(self.__ozon_brands_gen.set_index('Brand'), on='Brand')
            .rename({'Percent_x': 'Lamoda', 'Percent_y': 'Wildberries', 'Percent': 'Ozon'}, axis = 1)
            .reset_index()
        )
    
    def __plot_bar(self, fig, df, mp_name):
        fig.add_bar(
            x = df['Brand'],
            y = df[mp_name],
            name=mp_name
        )
        return fig

    def init_compare_dataframes(self, query):
        self.__query = query
        lamoda_brands = self.__get_brands_df(st.session_state.lamoda_df, query)
        wb_brands = self.__get_brands_df(st.session_state.wb_df, query)
        ozon_brands = self.__get_brands_df(st.session_state.ozon_df, query)
        self.__brand_intersection = self.__get_brand_intersection(lamoda_brands, wb_brands, ozon_brands)

        self.__lamoda_brands_gen = self.__df_filtering(lamoda_brands, self.__brand_intersection)
        self.__wb_brands_gen = self.__df_filtering(wb_brands, self.__brand_intersection)
        self.__ozon_brands_gen = self.__df_filtering(ozon_brands, self.__brand_intersection)
    
    def __set_category(self, df):
        return (
            df
            .assign(is_general = lambda x: x['Brand']
            .str.lower().map(lambda x: 'General' if x in self.__brand_intersection else 'Not in all MP'))
        )

    def __get_labeled_brands(self):
        lamoda_brands = self.__get_brands_df(st.session_state.lamoda_df, self.__query)
        wb_brands = self.__get_brands_df(st.session_state.wb_df, self.__query)
        ozon_brands = self.__get_brands_df(st.session_state.ozon_df, self.__query)

        return {'Lamoda': self.__set_category(lamoda_brands), 
                'Wildberries': self.__set_category(wb_brands), 
                'Ozon': self.__set_category(ozon_brands)}

    def df_st_printer(self, col, mp_name):
        col.markdown(f'#### {mp_name}')
        col.dataframe(self.__get_merged().set_index('Brand')[[mp_name]].sort_values(mp_name, ascending = False))

    def plotter_compare(self):
        fig = go.Figure()
        for mp_name in st.session_state.mp_names:
            fig = self.__plot_bar(fig, self.__get_merged(), mp_name)
        return fig
    
    def plotter_single(self):
        dfs = self.__get_labeled_brands()
        for mp_name in st.session_state.mp_names:
            df = dfs[mp_name].iloc[:40, :] 
            fig = px.bar(
                df,
                x = 'Brand',
                y = 'Percent',
                color = 'is_general',
                labels={
                    'is_general': 'Is general to all MP'
                },
                category_orders={
                    'Brand': df['Brand'],
                    'is_general': ['General', 'Not in all MP']
                },
                color_discrete_sequence=px.colors.qualitative.Dark24,
            )
            fig.update_layout(
                title = dict(
                    text = mp_name,
                    font = dict(
                        size = 20,
                        weight = 'bold'
                    )
                )
            )
            st.plotly_chart(fig)
                
... in main:
from streamlit_funcs.brand_compare import BrandCompare
                
brandCompare = BrandCompare()
brandCompare.init_compare_dataframes(search_var)

for col, mp_name in zip(st.columns([0.33, 0.33, 0.33]), ['Lamoda', 'Wildberries', 'Ozon']):
    brandCompare.df_st_printer(col, mp_name)

st.plotly_chart(brandCompare.plotter_compare())

brandCompare.plotter_single()

if st.checkbox('Show code snippets', value=False):
    brandCompare.code_printer()
''')
    
if __name__ == 'main':
    BrandCompare()