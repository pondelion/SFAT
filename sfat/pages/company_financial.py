import copy

import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

from ..st_cached_data import cached_financial_data


def company_financial():
    st.title('Company Financial')
    df_financial_data = cached_financial_data()
    latest_subdates_mask = df_financial_data.groupby(['証券コード'])['会計期間終了日'].transform('max') == df_financial_data['会計期間終了日']
    df_latest = df_financial_data[latest_subdates_mask]

    st.subheader('Raw Data')
    st.dataframe(df_latest.head(100))

    selected_item = st.selectbox(
        'Select Item',
        df_latest.columns.tolist(),
        11
    )
    min_val, max_val = st.slider(
        'Clip Data',
        min_value=float(df_latest[selected_item].min()),
        max_value=float(df_latest[selected_item].max()),
        value=(
            float(df_latest[selected_item].min()),
            float(df_latest[selected_item].quantile(0.995))
        ),
    )
    df_latest_clipped = df_latest.copy()
    df_latest_clipped[selected_item] = df_latest[selected_item].clip(min_val, max_val)
    st.header(selected_item)
    st.subheader(f'{selected_item} Distribution')
    plt.figure(figsize=(12, 6))
    sns.distplot(df_latest_clipped[selected_item], bins=80, kde=False)
    cols = st.columns([1, 20, 1])
    cols[1].pyplot(plt)

    st.subheader(f'{selected_item} Distribution by Sectors')
    plt.figure(figsize=(12, 5))
    sns.boxenplot(x='業種', y=selected_item, data=df_latest_clipped)
    plt.xticks(rotation=45)
    cols = st.columns([1, 20, 1])
    cols[1].pyplot(plt)

    st.subheader(f'Item Pairplot')
    selected_items = st.multiselect(
        'Select Items',
        df_latest.columns.tolist(),
        ['従業員数', '自己資本比率', '売上高', '株価収益率', '平均年齢']
    )
    plt.figure(figsize=(10, 10))
    sns.pairplot(df_latest[selected_items + ['業種']], hue='業種')
    cols = st.columns([1, 40, 1])
    cols[1].pyplot(plt)
