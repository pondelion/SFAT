import copy

import streamlit as st
import matplotlib.pyplot as plt

from ..datasets import EconomicIndicatorJA
from ..datasets.economic_indicator import IndicatorTypeJA


@st.cache
def econimic_indicator_ja_data():
    data_dict = {}
    for itja in IndicatorTypeJA:
        data_dict[itja.name] = EconomicIndicatorJA(itja)
    return data_dict


def economic_indicator():
    st.title('Economic Indocator')
    ei_ja_data = copy.deepcopy(econimic_indicator_ja_data())
    selected_indicators = st.multiselect(
        'Economic Indicator List',
        list(ei_ja_data.keys()),
        list(ei_ja_data.keys())
    )

    for i, si in enumerate(selected_indicators):
        # fig = plt.figure()
        # ei_ja_data[si].df().iloc[:, 0].plot(title=si)
        # st.pyplot(fig)
        if i % 3 == 0:
            cols = st.columns(3)
        cols[i%3].write(si)
        #cols[i%3].line_chart(ei_ja_data[si].df().iloc[:, 0])
        fig = plt.figure()
        ei_ja_data[si].df().iloc[:, 0].plot(title=si)
        cols[i%3].pyplot(fig)
