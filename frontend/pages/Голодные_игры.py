"""
Отдельная страница с подробной информацией о фильме «Голодные игры».
Использует общую функцию show_movie_details() из movie_details.py
"""

import streamlit as st

st.set_page_config(
    page_title="Голодные игры",
    layout="wide",
)

from movie_details import show_movie_details

show_movie_details("hungergames")