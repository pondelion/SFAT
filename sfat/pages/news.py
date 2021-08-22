from datetime import date, timedelta

import streamlit as st
import pandas as pd

from ..st_cached_data import cached_google_news


def news():
    st.title('News Analysis')

    min_dt, max_dt = st.slider(
        'Select date range',
        min_value=date.today() - timedelta(days=365),
        max_value=date.today(),
        value=(
            date.today() - timedelta(days=10),
            date.today()
        ),
        format='YYYY-MM-DD',
    )

    dates = pd.date_range(
        pd.to_datetime(min_dt),
        pd.to_datetime(max_dt),
        freq='D'
    )
    dfs = []
    for d in dates:
        dfs.append(cached_google_news(pub_date=d.date()))

    df = pd.concat(dfs).reset_index()
    st.dataframe(df)
