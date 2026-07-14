"""
Пример страницы с подробным описанием фильма.
Использует данные из movies_data.py
"""

import os
import streamlit as st
from movies_data import MOVIES
from nav import render_nav

BASE_DIR = os.path.dirname(os.path.abspath(__file__))


def asset_path(relative_path: str) -> str:
    return os.path.join(BASE_DIR, relative_path)


def load_css():
    css_path = os.path.join(BASE_DIR, "style.css")
    with open(css_path, encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def show_movie_details(movie_key: str):
    load_css()
    

    back_col, spacer = st.columns([1, 5])
    with back_col:
        st.page_link("pages/Фильмы.py", label="← Назад")

    movie = MOVIES.get(movie_key)

    if movie is None:
        st.error("Фильм не найден")
        return

    left_col, right_col = st.columns([1.4, 1], gap="large")

    with left_col:
        st.markdown(
            f"<h1 class='movie-title'>{movie['title']}</h1>",
            unsafe_allow_html=True,
        )
        st.markdown(
            f"<p class='movie-quote'>«{movie['quote']}»</p>",
            unsafe_allow_html=True,
        )

    with right_col:
        st.image(asset_path(movie["poster"]), use_container_width=True)

    st.markdown("<div class='movie-spacer'></div>", unsafe_allow_html=True)

    st.markdown("### О фильме")
    st.markdown(
        f"<p class='movie-description'>{movie['description']}</p>",
        unsafe_allow_html=True,
    )

    st.markdown("<div class='movie-spacer-small'></div>", unsafe_allow_html=True)

    col1, col2, col3, col4 = st.columns(4)

    metrics = [
        ("Жанр", movie["genre"]),
        ("Год", movie["year"]),
        ("Режиссёр", movie["director"]),
        ("Рейтинг", f"{movie['rating']} / 10"),
    ]

    for col, (label, value) in zip([col1, col2, col3, col4], metrics):
        with col:
            st.markdown(
                f"""
                <div class='metric-box'>
                    <div class='metric-label'>{label}</div>
                    <div class='metric-value'>{value}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("<div class='movie-spacer'></div>", unsafe_allow_html=True)
    st.markdown("### Актёры")
    actor_cols = st.columns(len(movie["actors"]), gap="medium")
    for col, actor in zip(actor_cols, movie["actors"]):
        with col:
            st.image(asset_path(actor["photo"]), use_container_width=True)
            st.markdown(
                f"<p class='actor-name'>{actor['name']}</p>",
                unsafe_allow_html=True,
            )
            st.markdown(
                f"<p class='actor-role'>{actor['role']}</p>",
                unsafe_allow_html=True,
            )

    st.markdown("<div class='movie-spacer'></div>", unsafe_allow_html=True)
    st.markdown("### Трейлер")
    st.markdown(
        f'<iframe width="100%" height="400" src="{movie["trailer_url"]}" '
        f'frameborder="0" allowfullscreen></iframe>',
        unsafe_allow_html=True,
    )