from datetime import timedelta

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import japanize_matplotlib
import seaborn as sns
import networkx as nx

from ..datasets import StockPrice
from ..st_cached_data import (
    cached_stocklist,
    cached_stockprice,
    cached_sampled_closes,
)
from ..widgets import (
    stock_selection_widget,
)


def code2company_name(code):
    df_stocklist = cached_stocklist()
    return df_stocklist[df_stocklist['銘柄コード']==int(code)]['銘柄名'].values[0]


def company_name2code(company_name):
    df_stocklist = cached_stocklist()
    return df_stocklist[df_stocklist['銘柄名']==company_name]['銘柄コード'].values[0]


def sector2color(sector, cmap_name='hsv'):
    df_stocklist = cached_stocklist()
    df_sector = pd.DataFrame({
        'sector': df_stocklist['業種分類'].unique()
    })
    n = df_sector[df_sector['sector']==sector].index.values[0]
    cmap = plt.cm.get_cmap(cmap_name, len(df_sector))
    return cmap(n)


def company_name2sector(company_name):
    df_stocklist = cached_stocklist()
    return df_stocklist[df_stocklist['銘柄名']==company_name]['業種分類'].values[0]


def draw_corr_network(node_names, corr, corr_thresh, fig_size=(12, 12)):
    graph = nx.Graph()
    graph.add_nodes_from(node_names)
    weighted_edges = []
    node_colors = [sector2color(company_name2sector(company_name)) for company_name in node_names]

    for i in range(corr.shape[0]):
        for j in range(corr.shape[1]):
            if i == j:
                continue
            if abs(corr[i, j]) >= corr_thresh:
                graph.add_edge(node_names[i], node_names[j], weight=abs(corr[i, j]), color='red')

    pos = nx.spring_layout(graph)

    plt.figure(figsize=fig_size)
    nx.draw_networkx(graph, pos, with_labels=True, node_color=node_colors, font_family="IPAexGothic")
    plt.axis("off")

    return graph


def stockprice():
    st.title('Stock Price Analysis')

    st.header('Correleation Analysis')
    df_stocklist = cached_stocklist()
    code, company_name = stock_selection_widget(
        df_stocklist,
        'Select Analysis Target Company'
    )
    df_target_stockprice = cached_stockprice(code=code)

    n_sampling = 50

    df_sampled_closes = cached_sampled_closes(n=n_sampling)
    st.write(f'Using {len(df_sampled_closes.columns)} random sampled stockprices for correlation calculation.')
    st.dataframe(df_sampled_closes.tail(100))

    df_closes = pd.merge(
        df_target_stockprice[['Close']].rename(columns={'Close': code}), df_sampled_closes,
        how='outer', left_index=True, right_index=True
    )

    min_dt, max_dt = st.slider(
        'Select date range',
        min_value=df_closes.index.min().date(),
        max_value=df_closes.index.max().date(),
        value=(
            max(df_closes.index.min().date(), df_closes.index.max().date()-timedelta(days=365)),
            df_closes.index.max().date()
        ),
        format='YYYY-MM-DD',
    )

    df_target_closes = df_closes[
        (df_closes.index.date >= min_dt) & (df_closes.index.date <= max_dt)
    ]

    st.subheader('Correleation Coefficient Heatmap')
    fig = plt.figure(figsize=(8, 8))
    df_corr = df_target_closes.corr(min_periods=30)
    sns.heatmap(df_corr, annot=True)
    cols = st.columns([1, 6, 1])
    cols[1].pyplot(fig)

    st.subheader('Correleation Coefficient Ranking')
    fig = plt.figure(figsize=(8, 5))
    df_corr_ranking = df_corr[code].sort_values(ascending=False)
    df_corr_ranking[1:][::-1].plot.barh()
    plt.yticks(
        range(len(df_corr_ranking)-1),
        [f'{code}/{code2company_name(code)}' for code in df_corr_ranking[1:][::-1].index.tolist()]
    )
    plt.xlabel('Correlation Coefficient')
    cols = st.columns([1, 12, 1])
    cols[1].pyplot(plt)

    st.subheader('Timeseries Comparison')
    selected_companies = st.multiselect(
        'Plot Target Company',
        [f'{code}/{code2company_name(code)}' for code in df_corr.index.tolist()],
        [f'{code}/{code2company_name(code)}' for code in df_corr_ranking[:2].index.tolist()]
    )
    selected_codes = [int(sc.split('/')[0]) for sc in selected_companies]
    fig = plt.figure(figsize=(12, 5))
    df_target_closes[selected_codes].plot()
    cols = st.columns([1, 10, 1])
    cols[1].pyplot(plt)

    st.subheader('Correleation Network')
    corr_thresh = st.slider('Correlation Threshold', 0.1, 1.0, 0.4)
    fig = plt.figure(figsize=(8, 8))
    node_names = [code2company_name(code) for code in df_corr.index.tolist()]
    draw_corr_network(node_names, df_corr.to_numpy(), corr_thresh)
    cols = st.columns([1, 6, 1])
    cols[1].pyplot(plt)
