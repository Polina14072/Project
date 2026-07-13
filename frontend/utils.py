import streamlit as st
import os
import base64
import mimetypes


def load_css(base_dir, css_relative_path="style.css"):

    css_path = os.path.join(base_dir, css_relative_path)

    with open(css_path, encoding="utf-8") as file:
        st.markdown(f"<style>{file.read()}</style>", unsafe_allow_html=True)


def get_image_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()


def get_mime_type(path):
    mime_type, _ = mimetypes.guess_type(path)
    return mime_type or "image/jpeg"


NAV_ITEMS = [
    ("Главная", "Главная.py"),
    ("Фильмы", "pages/Фильмы.py"),
    ("Отзывы", "pages/Отзывы.py"),
    ("Топ", "pages/Топ.py"),
    ("Регистрация", "pages/Регистрация.py"),
]


def render_nav(active_label):

    st.markdown('<div class="nav-bar">', unsafe_allow_html=True)

    col_logo, col_menu = st.columns([1, 3])

    with col_logo:
        st.markdown('<div class="small-logo">FILMS</div>', unsafe_allow_html=True)

    with col_menu:

        st.markdown('<div class="nav-menu">', unsafe_allow_html=True)

        cols = st.columns(len(NAV_ITEMS))

        for col, (label, path) in zip(cols, NAV_ITEMS):

            with col:

                if label == active_label:
                    st.button(label, key=f"nav_{label}", disabled=True)
                else:
                    if st.button(label, key=f"nav_{label}"):
                        st.switch_page(path)

        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    





    