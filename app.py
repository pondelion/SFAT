import streamlit as st

from sfat.utils.multi_page import MultiPage
from sfat.pages import (
    company_list,
    company_profile,
    economic_indicator,
    stockprice,
    company_announcement,
    company_financial,
    news,
)


def tmp_page():
    st.write('tmp page')


def main():
    multi_page = MultiPage()
    multi_page.add_page('Company List', company_list)
    multi_page.add_page('Company Profile', company_profile)
    multi_page.add_page('Company Announcement', company_announcement)
    multi_page.add_page('Stockprice', stockprice)
    multi_page.add_page('Financial Comparison', company_financial)
    multi_page.add_page('Cluster Analysis', tmp_page)
    multi_page.add_page('Economic Indicator', economic_indicator)
    multi_page.add_page('News Analysys', news)
    multi_page.add_page('Google/Twitter Trends Analysis', tmp_page)
    multi_page.add_page('Twitter Analysis', tmp_page)
    multi_page.add_page('Earthquake Analysis', tmp_page)
    multi_page.run()


if __name__ == '__main__':
    main()
