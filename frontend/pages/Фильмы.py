import os
import base64
import streamlit as st
from movies_data import MOVIES
from nav import render_nav

st.set_page_config(page_title="Фильмы", layout="wide")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def asset_path(relative_path: str) -> str:
    return os.path.join(BASE_DIR, relative_path)


def load_css():
    css_path = os.path.join(BASE_DIR, "style.css")
    with open(css_path, encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def set_background(image_relative_path: str):
    """Ставит затемнённую картинку фоном на всё приложение"""
    image_path = asset_path(image_relative_path)
    with open(image_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()

    ext = image_relative_path.split(".")[-1]
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: linear-gradient(rgba(0,0,0,0.7), rgba(0,0,0,0.7)),
                               url(data:image/{ext};base64,{encoded});
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


MOVIE_PAGES = {
    "avatar": "pages/Аватар.py",
    "inception": "pages/Начало.py",
    "hungergames": "pages/Голодные_игры.py",
}


load_css()

render_nav()

st.markdown(
    "<h1 style='color: white; text-align: center; margin-top: 1rem;'>Фильмы</h1>",
    unsafe_allow_html=True,
)

st.markdown("<div class='movie-spacer'></div>", unsafe_allow_html=True)

cols = st.columns(len(MOVIES))

for col, (movie_key, movie) in zip(cols, MOVIES.items()):
    with col:
        st.image(asset_path(movie["poster"]), use_container_width=True)
        st.markdown(
            f"<h3 style='color: white;'>{movie['title']}</h3>",
            unsafe_allow_html=True,
        )
        st.markdown(
            f"<p style='color: #cccccc;'>{movie['short_description']}</p>",
            unsafe_allow_html=True,
        )

        if st.button("Подробнее", key=f"details_{movie_key}", use_container_width=True):
            st.switch_page(MOVIE_PAGES[movie_key])