import streamlit as st
import pandas as pd

from ..st_cached_data import cached_stocklist


def company_list():
    st.title('Company List')
    df = cached_stocklist()
    sector_list = df['業種分類'].unique().tolist()
    selected_sector = st.selectbox(
        'Sector Filter',
        ['全て'] + sector_list
    )
    if selected_sector == '全て':
        selected_df = df
    else:
        selected_df = df[df['業種分類']==selected_sector]
    st.dataframe(selected_df)
    st.write(f'Company Counts of {selected_sector} : {len(selected_df)}')

    st.subheader('Company counts by sector')
    st.bar_chart(df['業種分類'].value_counts())