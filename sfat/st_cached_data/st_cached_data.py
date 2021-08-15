from typing import List

import streamlit as st
from fastprogress import progress_bar as pb
import pandas as pd

from ..datasets import (
    StockList,
    StockPrice,
    CompanyFinancials,
    CompanyFinancialsYFinance,
    CompanyAnnouncement,
)


@st.cache
def cached_stocklist():
    stocklist = StockList()
    df_stocklist = stocklist.df()
    return df_stocklist


@st.cache
def cached_stockprice(code: int):
    print(code)
    stockprice = StockPrice(code=code)
    df_stockprice = stockprice.df()
    return df_stockprice


@st.cache
def cached_closes(codes: List[int] = None):
    if codes is None:
        df_stocklist = cached_stocklist()
        codes = list(df_stocklist['銘柄コード'].unique())
    df_dict = {}
    skipped_code = []

    for code in pb(codes):
        try:
            df_dict[code] = cached_stockprice(code=code)[['Close']]
        except Exception:
            skipped_code.append(code)

    df_merged = None

    for code, df in pb(df_dict.items()):
        if df_merged is None:
            df_merged = df.rename(columns={'Close': code})
        else:
            df_merged = pd.merge(
                df_merged, df.rename(columns={'Close': code}),
                how='outer', left_index=True, right_index=True
            )
    return df_merged


@st.cache
def cached_sampled_closes(n: int):
    df_stocklist = cached_stocklist()
    codes = list(df_stocklist.sample(n)['銘柄コード'].unique())

    df_dict = {}
    skipped_code = []

    for code in pb(codes):
        try:
            df_dict[code] = cached_stockprice(code=code)[['Close']]
            # df_dict[code] = StockPrice(code=code).df()[['Close']]
        except Exception as e:
            print(e)
            skipped_code.append(code)

    df_merged = None

    for code, df in pb(df_dict.items()):
        if df_merged is None:
            df_merged = df.rename(columns={'Close': code})
        else:
            df_merged = pd.merge(
                df_merged, df.rename(columns={'Close': code}),
                how='outer', left_index=True, right_index=True
            )
    return df_merged


def sampled_closes(n: int):
    df_stocklist = cached_stocklist()
    codes = list(df_stocklist.sample(n)['銘柄コード'].unique())

    df_dict = {}
    skipped_code = []

    for code in pb(codes):
        try:
            # df_dict[code] = cached_stockprice(code=code)[['Close']]
            df_dict[code] = StockPrice(code=code).df()[['Close']]
        except Exception as e:
            print(e)
            skipped_code.append(code)

    df_merged = None

    for code, df in pb(df_dict.items()):
        if df_merged is None:
            df_merged = df.rename(columns={'Close': code})
        else:
            df_merged = pd.merge(
                df_merged, df.rename(columns={'Close': code}),
                how='outer', left_index=True, right_index=True
            )
    return df_merged


@st.cache
def cached_financial_data():
    df_company_financials = CompanyFinancials().df()
    df_company_financials['証券コード'] = df_company_financials['証券コード'].astype(int)
    return df_company_financials


@st.cache
def cached_financial_yfinance_data(code: int):
    financial = CompanyFinancialsYFinance(code=code)
    df_financial = financial.df()
    df_financial.set_index('Date', inplace=True)
    df_financial.sort_index(inplace=True)
    return df_financial


@st.cache
def cached_company_announcement(code: int):
    ca = CompanyAnnouncement(code=code)
    # ca_data = ca.json()
    ca_data = ca.df()
    return ca_data
