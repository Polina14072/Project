import streamlit as st
import os
import requests
from dotenv import load_dotenv
from streamlit_cookies_manager import EncryptedCookieManager
from nav import render_nav


st.set_page_config(
    page_title="FILMS | Фильмы 2.0",
    page_icon="FILMS",
    layout="centered"
)


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ENV_PATH = os.path.abspath(os.path.join(BASE_DIR, "..", ".env"))

load_dotenv(ENV_PATH)

with open(
    os.path.join(BASE_DIR, "style.css"),
    encoding="utf-8"
) as file:

    st.markdown(
        f"<style>{file.read()}</style>",
        unsafe_allow_html=True
    )


render_nav()


API_URL = "http://localhost:8000"


COOKIE_SECRET = os.environ.get("COOKIE_SECRET")

if not COOKIE_SECRET:
    st.error("Не задан COOKIE_SECRET в переменных окружения")
    st.code(
        f"Искал .env по пути: {ENV_PATH}\n"
        f"Файл существует: {os.path.exists(ENV_PATH)}"
    )
    st.stop()

cookies = EncryptedCookieManager(
    prefix="films_app_",
    password=COOKIE_SECRET
)
if not cookies.ready():
    st.stop()


def auth_headers():
    return {"Authorization": f"Bearer {st.session_state['access_token']}"}


def extract_error_message(response) -> str:
    try:
        error_data = response.json()
    except ValueError:
        return f"Код ошибки: {response.status_code}"

    detail = error_data.get("detail", "Неизвестная ошибка")

    if isinstance(detail, list):
        messages = [item.get("msg", str(item)) for item in detail]
        return "; ".join(messages)

    return detail


if "access_token" not in st.session_state:
    token = cookies.get("access_token")

    if token:
        st.session_state["access_token"] = token
    else:
        st.warning("Войдите в аккаунт, чтобы добавлять фильмы и отзывы")

        if st.button("Перейти к входу"):
            st.switch_page("pages/Вход.py")

        st.stop()


try:
    me_response = requests.get(
        f"{API_URL}/users/me",
        headers=auth_headers(),
        timeout=10,
    )

    if me_response.status_code != 200:
        st.session_state.pop("access_token", None)
        cookies["access_token"] = ""
        cookies.save()

        st.warning("Сессия истекла, войдите заново")

        if st.button("Перейти к входу"):
            st.switch_page("pages/Вход.py")

        st.stop()

    current_user = me_response.json()

except requests.exceptions.RequestException:
    st.error("Не удалось подключиться к серверу")
    st.stop()


st.markdown(
    """
    <div class="auth-title">

    <h1>
    Фильмы 2.0
    </h1>

    <p>
    Добавляйте фильмы и делитесь впечатлениями
    </p>

    </div>
    """,
    unsafe_allow_html=True
)


st.markdown('<div class="form-card">', unsafe_allow_html=True)

with st.form("add_film"):

    new_title = st.text_input(
        "Название фильма",
        placeholder="Введите название"
    )

    new_director = st.text_input(
        "Режиссёр",
        placeholder="Введите имя режиссёра"
    )

    add_film_submit = st.form_submit_button("Добавить фильм")

    if add_film_submit:

        if not new_title or not new_director:
            st.error("Заполните оба поля")

        else:
            try:
                create_response = requests.post(
                    f"{API_URL}/films/",
                    json={
                        "title": new_title,
                        "director": new_director
                    },
                    headers=auth_headers(),
                    timeout=10,
                )

                if create_response.status_code == 201:
                    st.success("Фильм добавлен!")
                    st.rerun()
                else:
                    st.error(
                        f"Не удалось добавить фильм: {extract_error_message(create_response)}"
                    )

            except requests.exceptions.RequestException:
                st.error("Не удалось подключиться к серверу")

st.markdown("</div>", unsafe_allow_html=True)


try:
    films_response = requests.get(f"{API_URL}/films/", timeout=10)
    ratings_response = requests.get(f"{API_URL}/ratings/", timeout=10)
    reviews_response = requests.get(f"{API_URL}/reviews/", timeout=10)

    films = films_response.json() if films_response.status_code == 200 else []
    all_ratings = ratings_response.json() if ratings_response.status_code == 200 else []
    all_reviews = reviews_response.json() if reviews_response.status_code == 200 else []

except requests.exceptions.RequestException:
    st.error("Не удалось загрузить список фильмов. Проверьте, что backend запущен.")
    st.stop()


st.markdown(
    """
    <div class="auth-title">
    <h1>Все фильмы</h1>
    </div>
    """,
    unsafe_allow_html=True
)


if not films:
    st.info("Фильмов пока нет. Добавьте первый!")


for film in films:

    film_ratings = [r for r in all_ratings if r["film_id"] == film["id"]]
    film_reviews = [r for r in all_reviews if r["film_id"] == film["id"]]

    my_review = next(
        (r for r in film_reviews if r["user_id"] == current_user["id"]),
        None
    )
    my_rating = next(
        (r for r in film_ratings if r["user_id"] == current_user["id"]),
        None
    )

    if film_ratings:
        average_score = sum(r["score"] for r in film_ratings) / len(film_ratings)
        rating_line = f"Средний рейтинг: {average_score:.1f}/10 ({len(film_ratings)} оценок)"
    else:
        rating_line = "Пока нет оценок"

    st.markdown('<div class="form-card">', unsafe_allow_html=True)

    st.markdown(f"### {film['title']}")
    st.markdown(f"Режиссёр: {film['director']}")
    st.markdown(rating_line)

    if my_review or my_rating:
        st.markdown("**Ваш отзыв:**")

        if my_rating:
            st.markdown(f"Оценка: {my_rating['score']}/10")

        if my_review:
            st.markdown(my_review["text"])

    else:
        with st.form(f"review_form_{film['id']}"):

            score = st.slider(
                "Оценка",
                min_value=1,
                max_value=10,
                value=5,
            )

            text = st.text_area(
                "Ваш отзыв",
                placeholder="Расскажите, что вам понравилось или нет..."
            )

            submit_review = st.form_submit_button("Опубликовать отзыв")

            if submit_review:

                if not text:
                    st.error("Напишите текст отзыва")

                else:
                    try:
                        rating_resp = requests.post(
                            f"{API_URL}/ratings/",
                            json={"score": score, "film_id": film["id"]},
                            headers=auth_headers(),
                            timeout=10,
                        )

                        review_resp = requests.post(
                            f"{API_URL}/reviews/",
                            json={"text": text, "film_id": film["id"]},
                            headers=auth_headers(),
                            timeout=10,
                        )

                        if rating_resp.status_code == 201 and review_resp.status_code == 201:
                            st.success("Отзыв опубликован!")
                            st.rerun()
                        else:
                            problems = []

                            if rating_resp.status_code != 201:
                                problems.append(extract_error_message(rating_resp))

                            if review_resp.status_code != 201:
                                problems.append(extract_error_message(review_resp))

                            st.error("Не удалось опубликовать отзыв: " + "; ".join(problems))

                    except requests.exceptions.RequestException:
                        st.error("Не удалось подключиться к серверу")

    other_reviews = [r for r in film_reviews if r["user_id"] != current_user["id"]]

    if other_reviews:
        st.markdown("**Другие отзывы:**")

        for review in other_reviews:
            matching_rating = next(
                (r for r in film_ratings if r["user_id"] == review["user_id"]),
                None
            )
            score_text = f"{matching_rating['score']}/10" if matching_rating else "—"

            st.markdown(f"Пользователь #{review['user_id']} ({score_text}): {review['text']}")

    st.markdown("</div>", unsafe_allow_html=True)