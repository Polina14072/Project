import streamlit as st
import os
import requests
from dotenv import load_dotenv
from streamlit_cookies_manager import EncryptedCookieManager


st.set_page_config(
    page_title="FILMS | Вход",
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


API_URL = "http://localhost:8000"


# --- cookies ---
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


def restore_session_from_cookie():
    token = cookies.get("access_token")

    if not token:
        return

    try:
        me_response = requests.get(
            f"{API_URL}/users/me",
            headers={"Authorization": f"Bearer {token}"},
            timeout=10,
        )

        if me_response.status_code == 200:
            user_data = me_response.json()

            st.session_state["access_token"] = token
            st.session_state["logged_in"] = True
            st.session_state["username"] = user_data.get("username")
            st.session_state["email"] = user_data.get("email")

            st.switch_page("pages/Главная.py")
        else:
            cookies["access_token"] = ""
            cookies.save()

    except requests.exceptions.RequestException:
        pass


restore_session_from_cookie()


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


# название сверху

st.markdown(
"""
<div class="small-logo">
FILMS
</div>
""",
unsafe_allow_html=True
)


# заголовок

st.markdown(
"""
<div class="auth-title">

<h1>
С возвращением
</h1>

<p>
Войдите в свой аккаунт
</p>

</div>
""",
unsafe_allow_html=True
)


# форма

with st.container():

    st.markdown(
    """
    <div class="form-card">
    """,
    unsafe_allow_html=True
    )

    with st.form(
        "login"
    ):

        email = st.text_input(
            "Email",
            placeholder="Введите email"
        )

        password = st.text_input(
            "Пароль",
            placeholder="Введите пароль",
            type="password"
        )

        remember_me = st.checkbox(
            "Запомнить меня",
            value=True
        )

        login = st.form_submit_button(
            "Войти"
        )

        if login:

            if not email or not password:
                st.error("Заполните все поля")

            else:
                try:
                    response = requests.post(
                        f"{API_URL}/auth/login",
                        json={
                            "email": email,
                            "password": password
                        },
                        timeout=10
                    )

                    if response.status_code == 200:

                        data = response.json()
                        token = data.get("access_token")

                        if token:
                            st.session_state["access_token"] = token
                            st.session_state["logged_in"] = True
                            st.session_state["email"] = email

                            if remember_me:
                                cookies["access_token"] = token
                                cookies.save()

                            st.success("Вход выполнен!")
                            st.switch_page("pages/Главная.py")

                        else:
                            st.error("Не удалось получить токен")

                    elif response.status_code == 401:
                        st.error("Неверный email или пароль")

                    else:
                        st.error(
                            f"Ошибка входа: {extract_error_message(response)}"
                        )

                except requests.exceptions.RequestException:
                    st.error("Не удалось подключиться к серверу")

    st.markdown(
    """
    </div>
    """,
    unsafe_allow_html=True
    )


# ссылка на регистрацию

st.markdown(
"""
<div class="login-link">
Ещё нет аккаунта?
</div>
""",
unsafe_allow_html=True
)
 