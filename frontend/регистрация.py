import streamlit as st
import os
import requests
from dotenv import load_dotenv
from streamlit_cookies_manager import EncryptedCookieManager


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_PATH = os.path.join(BASE_DIR, "..", ".env")
ENV_PATH = os.path.abspath(ENV_PATH)

load_dotenv(ENV_PATH)


st.set_page_config(
    page_title="FILMS | Регистрация",
    page_icon="FILMS",
    layout="centered"
)


with open(
    os.path.join(BASE_DIR, "style.css"),
    encoding="utf-8"
) as file:

    st.markdown(
        f"<style>{file.read()}</style>",
        unsafe_allow_html=True
    )


# --- адрес твоего FastAPI бэкенда ---
API_URL = "http://localhost:8000"


# --- cookies для "запомнить меня" ---
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



# центральный заголовок

st.markdown(
"""
<div class="auth-title">

<h1>
Создайте аккаунт
</h1>

<p>
Присоединяйтесь к миру кино
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
        "register"
    ):


        username = st.text_input(
            "Имя пользователя",
            placeholder="Введите имя"
        )


        email = st.text_input(
            "Email",
            placeholder="Введите email"
        )


        password = st.text_input(
            "Пароль",
            placeholder="Введите пароль",
            type="password"
        )


        confirm_password = st.text_input(
            "Подтвердите пароль",
            placeholder="Повторите пароль",
            type="password"
        )


        remember_me = st.checkbox(
            "Запомнить меня",
            value=True
        )


        register = st.form_submit_button(
            "Создать аккаунт"
        )



        if register:


            if not username or not email or not password:

                st.error(
                    "Заполните все поля"
                )


            elif password != confirm_password:

                st.error(
                    "Пароли не совпадают"
                )


            else:

                try:
                    response = requests.post(
                        f"{API_URL}/auth/register",
                        json={
                            "username": username,
                            "email": email,
                            "password": password
                        },
                        timeout=10
                    )

                    if response.status_code in (200, 201):

                        login_response = requests.post(
                            f"{API_URL}/auth/login",
                            json={
                                "email": email,
                                "password": password
                            },
                            timeout=10
                        )

                        if login_response.status_code == 200:

                            login_data = login_response.json()
                            token = login_data.get("access_token")

                            if token:
                                st.session_state["access_token"] = token
                                st.session_state["logged_in"] = True
                                st.session_state["username"] = username
                                st.session_state["email"] = email

                                if remember_me:
                                    cookies["access_token"] = token
                                    cookies.save()

                                st.success(
                                    "Аккаунт создан!"
                                )
                                st.switch_page("pages/Главная.py")

                            else:
                                st.error(
                                    "Аккаунт создан, но не удалось войти автоматически"
                                )

                        else:
                            st.error(
                                "Аккаунт создан, но вход не удался"
                            )

                    else:
                        st.error(
                            f"Ошибка регистрации: {extract_error_message(response)}"
                        )

                except requests.exceptions.RequestException:
                    st.error(
                        "Не удалось подключиться к серверу"
                    )


    st.markdown(
    """
    </div>
    """,
    unsafe_allow_html=True
    )



# ссылка на вход

st.markdown(
"""
<div class="login-link">
Уже есть аккаунт?
</div>
""",
unsafe_allow_html=True
)

col1, col2, col3 = st.columns([1, 1, 1])

with col2:
    if st.button("Перейти к входу", use_container_width=True):
        st.switch_page("pages/Вход.py")