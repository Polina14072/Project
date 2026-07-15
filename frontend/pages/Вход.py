import streamlit as st
import os
import requests
from streamlit_cookies_manager import EncryptedCookieManager


st.set_page_config(
    page_title="FILMS | Вход",
    page_icon="FILMS",
    layout="centered"
)


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

with open(
    os.path.join(BASE_DIR, "style.css"),
    encoding="utf-8"
) as file:

    st.markdown(
        f"<style>{file.read()}</style>",
        unsafe_allow_html=True
    )


API_URL = "http://localhost:8000"  # замени на реальный адрес


# --- cookies ---
cookies = EncryptedCookieManager(
    prefix="films_app_",
    password="замени_на_свой_секретный_ключ"
)
if not cookies.ready():
    st.stop()


# --- если уже есть токен — сразу на главную ---
if cookies.get("access_token"):
    st.session_state["access_token"] = cookies.get("access_token")
    st.session_state["logged_in"] = True
    st.switch_page("pages/Главная.py")



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

                st.error(
                    "Заполните все поля"
                )


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

                            st.success(
                                "Вход выполнен!"
                            )
                            st.switch_page("pages/Главная.py")

                        else:
                            st.error(
                                "Не удалось получить токен"
                            )

                    elif response.status_code == 401:
                        st.error(
                            "Неверный email или пароль"
                        )

                    else:
                        error_detail = response.json().get("detail", "Неизвестная ошибка")
                        st.error(
                            f"Ошибка входа: {error_detail}"
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



# ссылка на регистрацию

st.markdown(
"""
<div class="login-link">
Ещё нет аккаунта?
</div>
""",
unsafe_allow_html=True
)

col1, col2, col3 = st.columns([1, 1, 1])

with col2:
    if st.button("Перейти к регистрации", use_container_width=True):
        st.switch_page("регистрация.py")