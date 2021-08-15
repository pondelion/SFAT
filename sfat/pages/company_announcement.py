import streamlit as st
import numpy as np
import pandas as pd

from ..st_cached_data import (
    cached_stocklist,
    cached_company_announcement,
    cached_stockprice,
)
from ..widgets import stock_selection_widget


def company_announcement():
    st.title('Company Announcement')

    df_stocklist = cached_stocklist()
    code, company_name = stock_selection_widget(df_stocklist)

    ca_data = cached_company_announcement(code)

    st.subheader('Raw Data')
    # st.json(ca_data[:3])
    st.dataframe(ca_data)

    selected_return_days = st.multiselect(
        'Day for Return Calculation',
        range(1, 30),
        [1, 2, 3, 4]
    )

    df_stock = cached_stockprice(code).copy()

    df_stock['Open_lag1d'] = df_stock['Open'].shift(-1)
    for rd in selected_return_days:
        df_stock[f'Close_lag{rd}d'] = df_stock['Close'].shift(-rd)
        df_stock[f'change_rate_close{rd}_open'] = df_stock[f'Close_lag{rd}d'] / df_stock['Open_lag1d']

    crs = {f'rtn {rd}day': [] for rd in selected_return_days}

    for pd_ in ca_data['pubdate']:
        try:
            df_stock_target = df_stock[df_stock.index.date==pd_.date()]
            for rd in selected_return_days:
                crs[f'rtn {rd}day'].append(df_stock_target[f'change_rate_close{rd}_open'].values[0])
        except:
            for rd in selected_return_days:
                crs[f'rtn {rd}day'].append(np.nan)

    returns = {
        'pub_dates': ca_data['pubdate'],
        'titles': ca_data['title'],
    }
    returns.update(crs)
    df_returns = pd.DataFrame(returns)

    st.subheader('Stock Price Returns After Announcements')
    st.warning('リターンは適時開示日の翌営業日の始値に対するN日後の終値の変化率として計算しています。')
    dropna = st.checkbox('Exclude NA')
    if dropna:
        st.dataframe(df_returns.dropna())
    else:
        st.dataframe(df_returns)
