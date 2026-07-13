import streamlit as st
import os
import requests
from streamlit_cookies_manager import EncryptedCookieManager


st.set_page_config(
    page_title="FILMS | Профиль",
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


API_URL = "http://localhost:8000"

AVATAR_OPTIONS = ["🎬", "🍿", "🎭", "🎥", "⭐", "🦄", "🔥", "🌙", "🐱", "🚀"]


# --- cookies ---
cookies = EncryptedCookieManager(
    prefix="films_app_",
    password="замени_на_свой_секретный_ключ"
)
if not cookies.ready():
    st.stop()


if "access_token" not in st.session_state:
    token_from_cookie = cookies.get("access_token")
    if token_from_cookie:
        st.session_state["access_token"] = token_from_cookie
        st.session_state["logged_in"] = True


if not st.session_state.get("logged_in") or not st.session_state.get("access_token"):
    st.warning("Пожалуйста, войдите в аккаунт")
    if st.button("Перейти к входу"):
        st.switch_page("pages/login.py")
    st.stop()


token = st.session_state["access_token"]
headers = {"Authorization": f"Bearer {token}"}


# --- запрашиваем данные профиля с бэкенда ---
try:
    response = requests.get(
        f"{API_URL}/users/me",
        headers=headers,
        timeout=10
    )

    if response.status_code == 200:
        user_data = response.json()
        email = user_data.get("email", "—")
        role = user_data.get("role", "user")
        is_active = user_data.get("is_active", True)

    elif response.status_code == 401:
        st.session_state.clear()
        cookies["access_token"] = ""
        cookies.save()
        st.warning("Сессия истекла, войдите заново")
        if st.button("Перейти к входу"):
            st.switch_page("pages/login.py")
        st.stop()

    else:
        st.error("Не удалось загрузить данные профиля")
        st.stop()

except requests.exceptions.RequestException:
    st.error("Не удалось подключиться к серверу")
    st.stop()


# --- подтягиваем локально сохранённые имя и аватарку (из cookies) ---
username = cookies.get("username") or email.split("@")[0]
avatar = cookies.get("avatar") or "🎬"



# --- горизонтальное меню навигации ---

st.markdown(
"""
<div class="small-logo">
FILMS
</div>
""",
unsafe_allow_html=True
)

nav_col1, nav_col2, nav_col3, nav_col4, nav_col5 = st.columns(5)

with nav_col1:
    if st.button("Главная", use_container_width=True, key="nav_home"):
        st.switch_page("Главная.py")

with nav_col2:
    if st.button("Фильмы", use_container_width=True, key="nav_films"):
        st.switch_page("pages/Фильмы.py")

with nav_col3:
    if st.button("Отзывы", use_container_width=True, key="nav_reviews"):
        st.switch_page("pages/Отзывы.py")

with nav_col4:
    if st.button("Топ", use_container_width=True, key="nav_top"):
        st.switch_page("pages/Топ.py")

with nav_col5:
    if st.button("Профиль", use_container_width=True, key="nav_profile"):
        st.switch_page("pages/Профиль.py")

st.markdown("<br>", unsafe_allow_html=True)



if "editing_profile" not in st.session_state:
    st.session_state["editing_profile"] = False



if not st.session_state["editing_profile"]:

    # --- обычный просмотр профиля ---

    st.markdown(
    f"""
    <div class="auth-title">

    <div class="profile-avatar">
    {avatar}
    </div>

    <h1>
    {username}
    </h1>

    <p>
    {email}
    </p>

    </div>
    """,
    unsafe_allow_html=True
    )


    with st.container():

        st.markdown(
        """
        <div class="form-card">
        """,
        unsafe_allow_html=True
        )

        role_label = "Администратор" if role == "admin" else "Пользователь"
        status_label = "Активен" if is_active else "Неактивен"
        status_class = "badge-active" if is_active else "badge-inactive"

        st.markdown(
        f"""
        <div class="profile-info-row"><span class="profile-info-label">Email</span>
            <span class="profile-info-value">{email}</span>
        </div>

        <div class="profile-info-row">
            <span class="profile-info-label">Роль</span>
            <span class="profile-badge">{role_label}</span>
        </div>

        <div class="profile-info-row">
            <span class="profile-info-label">Статус</span>
            <span class="profile-badge {status_class}">{status_label}</span>
        </div>
        """,
        unsafe_allow_html=True
        )

        st.markdown(
        """
        </div>
        """,
        unsafe_allow_html=True
        )


    st.markdown("<br>", unsafe_allow_html=True)

    edit_col1, edit_col2, edit_col3 = st.columns([1, 1, 1])

    with edit_col2:
        if st.button("Редактировать профиль", use_container_width=True):
            st.session_state["editing_profile"] = True
            st.rerun()



else:

    # --- режим редактирования ---

    st.markdown(
    """
    <div class="auth-title">

    <h1>
    Редактировать профиль
    </h1>

    </div>
    """,
    unsafe_allow_html=True
    )


    with st.container():

        st.markdown(
        """
        <div class="form-card">
        """,
        unsafe_allow_html=True
        )

        new_username = st.text_input(
            "Имя пользователя",
            value=username
        )

        st.markdown("**Выберите аватарку**")

        selected_avatar = st.radio(
            "Аватар",
            options=AVATAR_OPTIONS,
            index=AVATAR_OPTIONS.index(avatar) if avatar in AVATAR_OPTIONS else 0,
            horizontal=True,
            label_visibility="collapsed"
        )

        st.markdown(
        """
        </div>
        """,
        unsafe_allow_html=True
        )


    save_col1, save_col2, save_col3 = st.columns([1, 1, 1])

    with save_col2:
        if st.button("Сохранить", use_container_width=True):

            cookies["username"] = new_username
            cookies["avatar"] = selected_avatar
            cookies.save()

            st.session_state["editing_profile"] = False
            st.success("Профиль обновлён!")
            st.rerun()


    cancel_col1, cancel_col2, cancel_col3 = st.columns([1, 1, 1])

    with cancel_col2:
        if st.button("Отмена", use_container_width=True):
            st.session_state["editing_profile"] = False
            st.rerun()



# кнопка выхода (только в режиме просмотра)

if not st.session_state["editing_profile"]:

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1, 1])

    with col2:
        if st.button("Выйти из аккаунта", use_container_width=True):
            st.session_state.clear()
            cookies["access_token"] = ""
            cookies.save()
            st.switch_page("pages/login.py")