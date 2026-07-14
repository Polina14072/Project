"""
Отдельная страница с подробной информацией о фильме «Начало».
Использует общую функцию show_movie_details() из movie_details.py
"""

import streamlit as st

st.set_page_config(
    page_title="Начало",
    layout="wide",
)

from movie_details import show_movie_details

show_movie_details("inception")