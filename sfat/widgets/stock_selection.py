import streamlit as st
import pandas as pd


def stock_selection_widget(
    df_stocklist: pd.DataFrame,
    title: str = 'Stock Selection'
):
    stock_select_method = st.radio(
        title,
        ('Select From List', 'Search From Code/Company Name Keyword')
    )
    if stock_select_method == 'Select From List':
        sector_col, company_col = st.columns([1, 2])

        sector_list = df_stocklist['業種分類'].unique().tolist()
        selected_sector = sector_col.selectbox(
            'Sector Filter',
            ['全て'] + sector_list
        )
        if selected_sector == '全て':
            selected_df = df_stocklist
        else:
            selected_df = df_stocklist[df_stocklist['業種分類']==selected_sector]

        selected_company = company_col.selectbox(
            'Company Selection',
            selected_df.apply(
                lambda x: f"{x['銘柄コード']}/{x['銘柄名']}",
                axis=1
            )
        )
    elif stock_select_method == 'Search From Code/Company Name Keyword':
        keyword = st.text_input('Code / Company Name', 'Fill in code or company name here.')
        df_selected_company = df_stocklist[
            df_stocklist['銘柄名'].str.contains(keyword) | df_stocklist['銘柄コード'].astype(str).str.contains(keyword)
        ]
        st.dataframe(df_selected_company)
        selected_company = st.selectbox(
            'Company Selection',
            df_selected_company.apply(
                lambda x: f"{x['銘柄コード']}/{x['銘柄名']}",
                axis=1
            )
        )
        if len(df_selected_company) == 0:
            st.stop()
    code, company_name = selected_company.split('/')
    code = int(code)
    return code, company_name