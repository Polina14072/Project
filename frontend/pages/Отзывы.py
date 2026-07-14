import os
import requests
import streamlit as st
from utils import load_css, render_nav
from streamlit_cookies_manager import EncryptedCookieManager

st.set_page_config(page_title="FILMS | Отзывы", layout="wide")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_css(BASE_DIR, "style.css")
render_nav("Отзывы")

API_URL = "http://localhost:8000"  # проверь, что совпадает с твоим реальным адресом

cookies = EncryptedCookieManager(
    prefix="films_app_",
    password="замени_на_свой_секретный_ключ"
)
if not cookies.ready():
    st.stop()

token = st.session_state.get("access_token") or cookies.get("access_token")


# --- Заголовок ---
st.markdown(
    """
    <div class="movies-title">
        <h1>ОТЗЫВЫ</h1>
        <p>Поделитесь впечатлениями о любимых фильмах</p>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown("<div class='movie-spacer'></div>", unsafe_allow_html=True)


# --- Получаем список фильмов с backend (для выбора film_id) ---
films_by_title = {}
try:
    films_response = requests.get(f"{API_URL}/films", timeout=10)
    if films_response.status_code == 200:
        films_list = films_response.json()
        films_by_title = {film["title"]: film["id"] for film in films_list}
except requests.exceptions.RequestException:
    pass


# --- Форма добавления отзыва ---
if not token:
    st.info("Войдите в аккаунт, чтобы оставить отзыв.")
    if st.button("Перейти к входу"):
        st.switch_page("pages/Вход.py")

elif not films_by_title:
    st.warning(
        "Не удалось загрузить список фильмов для отзыва. "
        "Проверьте, что backend запущен и эндпоинт /films доступен."
    )

else:
    with st.container():
        st.markdown("<div class='form-card'>", unsafe_allow_html=True)

        with st.form("add_review", clear_on_submit=True):
            st.markdown("### Оставить отзыв")

            selected_title = st.selectbox(
                "Выберите фильм",
                options=list(films_by_title.keys())
            )

            rating = st.slider(
                "Оценка",
                min_value=1,
                max_value=10,
                value=8
            )

            text = st.text_area(
                "Ваш отзыв",
                placeholder="Расскажите, что вам понравилось или нет...",
                height=120
            )

            submitted = st.form_submit_button("Опубликовать отзыв")

            if submitted:
                if not text:
                    st.error("Напишите текст отзыва")
                else:
                    film_id = films_by_title[selected_title]

                    try:
                        response = requests.post(
                            f"{API_URL}/reviews",
                            json={
                                "film_id": film_id,
                                "rating": rating,
                                "text": text,
                            },
                            headers={"Authorization": f"Bearer {token}"},
                            timeout=10,
                        )

                        if response.status_code in (200, 201):
                            st.success("Отзыв опубликован!")
                            st.rerun()
                        elif response.status_code == 401:
                            st.error("Сессия истекла, войдите заново")
                        else:
                            detail = response.json().get("detail", "Неизвестная ошибка")
                            st.error(f"Ошибка: {detail}")

                    except requests.exceptions.RequestException:
                        st.error("Не удалось подключиться к серверу")

        st.markdown("</div>", unsafe_allow_html=True)

st.markdown("<div class='movie-spacer'></div>", unsafe_allow_html=True)


# --- Список отзывов ---
st.markdown("### Все отзывы")

try:
    response = requests.get(f"{API_URL}/reviews", timeout=10)

    if response.status_code == 200:
        reviews = response.json()

        if not reviews:
            st.write("Пока нет ни одного отзыва.Будьте первым!")

        for review in reviews:
            rating_value = review.get("rating", 0)
            stars = "★" * rating_value + "☆" * (10 - rating_value)

            st.markdown(
                f"""
                <div class="review-card">
                    <div class="review-header">
                        <span class="review-movie">{review.get("film_title", review.get("film_id", "—"))}</span>
                        <span class="review-stars">{stars}</span>
                    </div>
                    <p class="review-author">{review.get("author_email", "Аноним")}</p>
                    <p class="review-text">{review.get("text", "")}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )
    else:
        st.warning("Не удалось загрузить отзывы")

except requests.exceptions.RequestException:
    st.error("Не удалось подключиться к серверу")