import copy
import time
from datetime import timedelta

import streamlit as st
import matplotlib.pyplot as plt
import pandas as pd

from ..st_cached_data import (
    cached_stocklist,
    cached_stockprice,
    cached_financial_data,
    cached_financial_yfinance_data,
)
from ..widgets import (
    stock_selection_widget,
)


def company_profile():
    st.title('Company Profile')
    st.header('Company Selection')
    df_stocklist = cached_stocklist()
    code, company_name = stock_selection_widget(df_stocklist)

    st.markdown('---')
    st.header(f'{company_name} Summary')
    df_stockprice = copy.deepcopy(cached_stockprice(code))
    st.subheader('Stockprice')
    st.markdown('- Raw Data')
    st.dataframe(df_stockprice)

    min_dt, max_dt = st.slider(
        'Select date range',
        min_value=df_stockprice.index.min().date(),
        max_value=df_stockprice.index.max().date(),
        value=(
            max(df_stockprice.index.min().date(), df_stockprice.index.max().date()-timedelta(days=365*2)),
            df_stockprice.index.max().date()
        ),
        format='YYYY-MM-DD',
    )

    df_target = df_stockprice[
        (df_stockprice.index.date >= min_dt) & (df_stockprice.index.date <= max_dt)
    ]
    st.markdown('- Stock Price Timeseries')
    fig = plt.figure(figsize=(12, 5))
    ax1 = fig.add_subplot(111)
    ax1.bar(df_target.index, df_target['Volume'], alpha=0.6)
    ax2 = ax1.twinx()
    ax2.plot(df_target.index, df_target['Close'], marker='o')
    st.pyplot(fig)

    # st.line_chart(df_stockprice[
    #     (df_stockprice.index.date >= min_dt) & (df_stockprice.index.date <= max_dt)
    # ][['Close', 'Open', 'High', 'Low']])

    # st.subheader('Volume')
    # st.bar_chart(df_stockprice[
    #     (df_stockprice.index.date >= min_dt) & (df_stockprice.index.date <= max_dt)
    # ]['Volume'])

    st.markdown('- Close Returns and Volumne Change Timeseries')
    fig = plt.figure(figsize=(12, 5))
    plt.plot(
        df_target.index,
        df_target['Volume'].pct_change()/df_target['Volume'].pct_change().max(),
        marker='o', alpha=0.6, label='volume change'
    )
    plt.plot(
        df_target.index,
        df_target['Close'].pct_change()/df_target['Close'].pct_change().max(),
        marker='o', alpha=0.6, label='close return'
    )
    plt.legend()
    st.pyplot(fig)

    st.markdown('- Tommorow Close Returns and Volumne Change Distribution')
    selected_corr_lag = st.selectbox(
        'Select Time Lag (day) for Correlation Calculation',
        [f'{day}day' for day in range(1, 30+1)]
    )
    corr_lag = int(selected_corr_lag.replace('day', ''))
    fig = plt.figure(figsize=(6, 6))
    plt.scatter(
        df_target['Volume'].pct_change(),
        df_target['Close'].pct_change().shift(int(corr_lag))
    )
    corr = pd.DataFrame(
        [df_target['Volume'].pct_change(), df_target['Close'].pct_change().shift(-int(corr_lag))]
    ).T.corr().iloc[0,1]
    plt.title(f'lag_{int(corr_lag)}, corr : {corr:.3f}')
    plt.xlabel('Volume Change')
    plt.ylabel('Tommorow Close Returns')
    cols = st.columns([1, 4, 1])
    cols[1].pyplot(fig)
    st.write(f'Correlation Coefficient : {corr:.3f}')

    st.subheader('Financials')
    # df_financials = cached_financial_data()
    # st.dataframe(df_financials[df_financials['証券コード']==code])
    df_financials = cached_financial_yfinance_data(code)
    st.dataframe(df_financials)

    fig = plt.figure()
    df_financials[
        ['Total Revenue', 'Gross Profit', 'Operating Income', 'Net Income']
    ].plot.bar(figsize=(12, 5), alpha=0.6)
    st.pyplot(plt)
