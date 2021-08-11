import streamlit as st

from utils.multi_page import MultiPage


def page1():
    st.write('page1')


def page2():
    st.write('page2')


def main():
    multi_page = MultiPage()
    multi_page.add_page('Page1', page1)
    multi_page.add_page('Page2', page2)
    multi_page.run()


if __name__ == '__main__':
    main()
