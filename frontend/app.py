import streamlit as st
import os
import requests
from streamlit_cookies_manager import EncryptedCookieManager


st.set_page_config(
    page_title="FILMS | Регистрация",
    page_icon="FILMS",
    layout="centered"
)


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

with open(
    os.path.join(BASE_DIR, "style.css"),
    encoding="utf-8"
) as file:

    st.markdown(
        f"<style>{file.read()}</style>",
        unsafe_allow_html=True
    )


# --- адрес твоего FastAPI бэкенда ---
API_URL = "http://localhost:8000"  # замени на реальный адрес


# --- cookies для "запомнить меня" ---
cookies = EncryptedCookieManager(
    prefix="films_app_",
    password="замени_на_свой_секретный_ключ"  # лучше вынести в .env
)
if not cookies.ready():
    st.stop()


# --- если токен уже есть в cookies — сразу пропускаем регистрацию ---
if cookies.get("access_token"):
    st.session_state["access_token"] = cookies.get("access_token")
    st.session_state["logged_in"] = True
    st.switch_page("pages/Профиль.py")



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
                    # шаг 1: регистрация (бэкенд принимает только email и password)
                    response = requests.post(
                        f"{API_URL}/auth/register",
                        json={
                            "email": email,
                            "password": password
                        },
                        timeout=10
                    )

                    if response.status_code in (200, 201):

                        # шаг 2: сразу логинимся, чтобы получить токен
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
                                st.switch_page("pages/Профиль.py")

                            else:
                                st.error(
                                    "Аккаунт создан, но не удалось войти автоматически"
                                )

                        else:
                            st.error(
                                "Аккаунт создан, но вход не удался"
                            )

                    else:
                        error_detail = response.json().get("detail", "Неизвестная ошибка")
                        st.error(
                            f"Ошибка регистрации: {error_detail}"
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
        st.switch_page("pages/login.py")
