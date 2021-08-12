from typing import Callable

import streamlit as st


class MultiPage:

    def __init__(self):
        self._pages = {}

    def add_page(self, name, func: Callable[[], None]):
        self._pages[name] = func

    def run(self):
        page = st.sidebar.radio(
            'CONTENTS',
            list(self._pages.keys())
        )
        self._pages[page]()
