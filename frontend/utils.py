import os
import streamlit as st


def load_css(base_dir: str, css_relative_path: str):
    """Подключает CSS-файл по пути относительно base_dir"""
    css_path = os.path.join(base_dir, css_relative_path)
    with open(css_path, encoding="utf-8") as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


def render_nav(current_page: str = ""):
    """Горизонтальное меню навигации.
    Последняя кнопка выделена (с фоном):
    - 'Регистрация', если пользователь не залогинен
    - 'Профиль', если пользователь уже вошёл в аккаунт"""

    pages = [
        ("Главная", "pages/Главная.py"),
        ("Фильмы", "pages/Фильмы.py"),
        ("Отзывы", "pages/Отзывы.py"),
        ("Топ", "pages/Топ.py"),
    ]

    is_logged_in = st.session_state.get("logged_in", False)

    st.markdown("<div class='nav-wrapper'>", unsafe_allow_html=True)

    cols = st.columns(len(pages) + 1)

    for col, (label, path) in zip(cols[:-1], pages):
        with col:
            st.page_link(path, label=label)

    with cols[-1]:
        if is_logged_in:
            st.page_link("pages/Профиль.py", label="Профиль")
        else:
            st.page_link("pages/Вход.py", label="Регистрация")

    st.markdown("</div>", unsafe_allow_html=True)

    





    