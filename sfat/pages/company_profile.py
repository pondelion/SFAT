import copy
import time

import streamlit as st
import matplotlib.pyplot as plt

from .company_list import cached_stocklist
from ..datasets import (
    StockPrice,
    CompanyFinancials,
)


@st.cache
def cached_stockprice(code: int):
    print(code)
    stockprice = StockPrice(code=code)
    df_stockprice = stockprice.df()
    return df_stockprice


@st.cache
def cached_financial_date():
    df_company_financials = CompanyFinancials().df()
    df_company_financials['証券コード'] = df_company_financials['証券コード'].astype(int)
    return df_company_financials


def company_profile():
    st.title('Company Profile')
    st.header('Company Selection')
    df_stocklist = cached_stocklist()
    stock_select_method = st.radio(
        'Stock Selection',
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

    st.markdown('---')
    st.header('Summary')
    code, company_name = selected_company.split('/')
    code = int(code)
    df_stockprice = copy.deepcopy(cached_stockprice(code))
    st.subheader('Stockprice')
    st.dataframe(df_stockprice)

    # fig = plt.figure()
    # df_stockprice['Close'].plot()
    # # plt.plot(df_stockprice['Close'])
    # st.pyplot(fig)
    st.line_chart(df_stockprice[['Close', 'Open', 'High', 'Low']])

    st.subheader('Volume')
    st.bar_chart(df_stockprice['Volume'])

    st.subheader('Financials')
    df_financials = cached_financial_date()
    st.dataframe(df_financials[df_financials['証券コード']==code])
