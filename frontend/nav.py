import streamlit as st


def render_nav():
    """Горизонтальное меню навигации без логотипа,
    текстовые ссылки на равном расстоянии друг от друга"""
    st.markdown("<div class='nav-wrapper'>", unsafe_allow_html=True)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
        st.page_link("pages/Главная.py", label="Главная")
    with col2:
        st.page_link("pages/Фильмы.py", label="Фильмы")
    with col3:
        st.page_link("pages/Отзывы.py", label="Отзывы")
    with col4:
        st.page_link("pages/Топ.py", label="Топ")
    with col5:
        st.page_link("pages/Фильмы_2.0.py", label="Фильмы 2.0")

    st.markdown("</div>", unsafe_allow_html=True)