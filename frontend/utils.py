import os
import streamlit as st


def load_css(base_dir: str, css_relative_path: str):
    """Подключает CSS-файл по пути относительно base_dir"""
    css_path = os.path.join(base_dir, css_relative_path)
    with open(css_path, encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def render_nav(current_page: str = ""):
    """Горизонтальное меню навигации без фона.
    При наведении ссылка приподнимается и становится красной.
    current_page — название текущей страницы (для подсветки активного пункта)"""

    pages = [
        ("Главная", "pages/Главная.py"),
        ("Фильмы", "pages/Фильмы.py"),
        ("Отзывы", "pages/Отзывы.py"),
        ("Топ", "pages/Топ.py"),
    ]

    st.markdown("<div class='nav-wrapper'>", unsafe_allow_html=True)
    cols = st.columns(len(pages))

    for col, (label, path) in zip(cols, pages):
        with col:
            st.page_link(path, label=label)

    st.markdown("</div>", unsafe_allow_html=True)

    





    