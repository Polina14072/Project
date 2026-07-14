import os
import base64
import streamlit as st
from nav import render_nav

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def load_css():
    css_path = os.path.join(BASE_DIR, "style.css")
    with open(css_path, encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def set_background(image_relative_path: str):
    """Ставит затемнённую картинку фоном на всё приложение"""
    image_path = os.path.join(BASE_DIR, image_relative_path)
    with open(image_path, "rb") as f:
        encoded = base64.b64encode(f.read()).decode()

    ext = image_relative_path.split(".")[-1]
    st.markdown(
        f"""
        <style>
        .stApp {{
            background-image: linear-gradient(rgba(0,0,0,0.6), rgba(0,0,0,0.6)),
                               url(data:image/{ext};base64,{encoded});
            background-size: cover;
            background-position: center;
            background-attachment: fixed;
        }}
        </style>
        """,
        unsafe_allow_html=True,
    )


st.set_page_config(page_title="FILMS", layout="wide")

load_css()
set_background("assets/main.png")

render_nav()

st.markdown("<div class='hero-content'>", unsafe_allow_html=True)

st.markdown(
    "<h1 style='font-size: 3rem; color: white; margin-top: 2rem;'>"
    "ФИЛЬМЫ, КОТОРЫЕ МЕНЯЮТ РЕАЛЬНОСТЬ</h1>",
    unsafe_allow_html=True,
)
st.markdown(
    "<p style='font-size: 1.2rem; color: #dddddd;'>"
    "Истории, которые остаются в памяти навсегда</p>",
    unsafe_allow_html=True,
)

st.markdown("</div>", unsafe_allow_html=True)