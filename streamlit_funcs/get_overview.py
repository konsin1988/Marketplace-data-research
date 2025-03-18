import pandas as pd
import streamlit as st
import plotly.express as px
import io

def get_overview(mp_var, pt_var):
    st.subheader(f'{mp_var} dataframe overview')
    mp_dict = st.session_state.marketplaces
    df = mp_dict[mp_var].query(f'SearchQuery == "{pt_var}"')

    st.text('Head of dataset')
    st.dataframe(df.head())

    col_info, col_na = st.columns([0.5, 0.5])

    col_info.text('Dataframe info')
    buffer = io.StringIO()
    df.info(buf=buffer)
    lines = buffer.getvalue().splitlines()
    info_df = (pd.DataFrame([x.split() for x in lines[5:-2]], columns=lines[3].split())
        .drop('Count',axis=1)
       .rename(columns={'Non-Null':'Non-Null Count', '#': '№'})
       .set_index('№')
       )
    col_info.write(info_df) 

    col_na.text('Total NA values')
    col_na.dataframe(df.isna().sum().to_frame().rename({0: 'NA numbers'}, axis=1))

    st.text(f'Duplicates count: {df.duplicated().sum()}')

    st.subheader('Value counts of categorical variables')
    col_radio, col_value_counts_data = st.columns([0.3, 0.7])
    value_counts_var = col_radio.radio('Variable', ('Brand', 'Gender', 'ProductName'))
    col_value_counts_data.dataframe(df[value_counts_var].value_counts().to_frame())

    st.subheader('Describe categorical variables')
    st.dataframe(df.select_dtypes('object').describe())
    
    st.subheader('Describe numeric variables')
    st.dataframe(df.select_dtypes('number').describe())

    col_plot_radio, col_plots = st.columns([0.3, 0.7])
    plot_variable = col_plot_radio.radio('Variable:', [*df.columns[1:3],  *df.columns[4:]])
    if df[plot_variable].dtype == 'object':
        col_plots.plotly_chart(
            px.bar(
                df[plot_variable].value_counts()[:20].to_frame().reset_index(),
                x = plot_variable,
                y = 'count'
            )
        )
    else:
        col_plots.plotly_chart(
            px.histogram(
                df.dropna()[[plot_variable]],
                x = plot_variable,
                nbins=90
            )
        )
        col_plots.plotly_chart(
            px.box(
                df[[plot_variable]],
                y = plot_variable
            )
        )

if __name__ == 'main':
    get_overview()