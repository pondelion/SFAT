import streamlit as st

from ..st_cached_data import (
    cached_stocklist,
    cached_company_announcement,
)
from ..widgets import stock_selection_widget


def company_announcement():
    st.title('Company Announcement')

    df_stocklist = cached_stocklist()
    code, company_name = stock_selection_widget(df_stocklist)

    ca_data = cached_company_announcement(code)

    st.json(ca_data)
