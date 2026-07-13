import streamlit as st
import os
import json
from datetime import datetime
from utils import load_css, render_nav


st.set_page_config(
    page_title="FILMS | Отзывы",
    layout="wide"
)


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_css(BASE_DIR, os.path.join("..", "style.css"))

render_nav("Отзывы")


REVIEWS_PATH = os.path.join(BASE_DIR, "..", "reviews.json")

MOVIES = ["Аватар", "Начало", "Голодные игры"]

AVATAR_COLORS = ["#FF6B6B", "#4ECDC4", "#556FB5", "#F7B801", "#9B59B6", "#2ECC71"]



def load_reviews():

    if not os.path.exists(REVIEWS_PATH):
        return []

    with open(REVIEWS_PATH, encoding="utf-8") as file:
        return json.load(file)



def save_reviews(reviews):

    with open(REVIEWS_PATH, "w", encoding="utf-8") as file:
        json.dump(reviews, file, ensure_ascii=False, indent=2)



def get_avatar_color(name):

    index = sum(ord(ch) for ch in name) % len(AVATAR_COLORS)
    return AVATAR_COLORS[index]



st.markdown(
"""
<div class="movies-title">
<h1>ОТЗЫВЫ</h1>
<p>Фильмы, которые остаются в памяти навсегда</p>
</div>
""",
unsafe_allow_html=True
)


reviews = load_reviews()



# --- форма добавления отзыва ---

with st.container():

    st.markdown('<div class="form-card">', unsafe_allow_html=True)

    st.markdown('<h3 class="form-title">✍️ Оставить отзыв</h3>', unsafe_allow_html=True)

    with st.form("add_review", clear_on_submit=True):

        movie = st.selectbox("Фильм", MOVIES)

        col_a, col_b = st.columns(2)

        with col_a:
            name = st.text_input("Ваше имя", placeholder="Введите имя")

        with col_b:
            rating = st.slider("Оценка", min_value=1, max_value=5, value=5)

        text = st.text_area("Ваш отзыв", placeholder="Поделитесь впечатлениями о фильме")

        submit = st.form_submit_button("Отправить отзыв")

        if submit:

            if not name or not text:
                st.error("Заполните все поля")

            else:
                reviews.append({
                    "movie": movie,
                    "name": name,
                    "rating": rating,
                    "text": text,
                    "date": datetime.now().strftime("%d.%m.%Y")
                })

                save_reviews(reviews)
                st.success("Спасибо за отзыв! 🎬")
                st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)


st.write("")
st.write("")



# --- отзывы, сгруппированные по фильму ---

if not reviews:

    st.markdown(
    """
    <div class="empty-state">
    <span class="empty-icon">🎥</span>
    <p>Пока нет отзывов. Будьте первым, кто поделится впечатлением!</p>
    </div>
    """,
    unsafe_allow_html=True
    )

else:

    for movie in MOVIES:

        movie_reviews = [r for r in reviews if r.get("movie") == movie]

        if not movie_reviews:
            continue

        avg_rating = sum(r["rating"] for r in movie_reviews) / len(movie_reviews)
        full_stars = round(avg_rating)
        avg_stars = "★" * full_stars + "☆" * (5 - full_stars)

        rating_class = "rating-high" if avg_rating >= 4 else "rating-mid" if avg_rating >= 2.5 else "rating-low"

        st.markdown(
        f"""
        <div class="movie-review-header">
            <div class="movie-review-title">
                <h2>{movie}</h2>
                <span class="review-count">{len(movie_reviews)} отзыв(ов)</span>
            </div>
            <div class="avg-badge {rating_class}">
                <span class="avg-stars">{avg_stars}</span>
                <span class="avg-number">{avg_rating:.1f}</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True
        )

        cols = st.columns(min(len(movie_reviews), 3))

        for idx, review in enumerate(reversed(movie_reviews)):

            stars = "★" * review["rating"] + "☆" * (5 - review["rating"])
            initial = review["name"][0].upper()
            color = get_avatar_color(review["name"])

            with cols[idx % len(cols)]:

                st.markdown(
                f"""<div class="review-card">
                    <div class="review-card-top">
                        <div class="review-avatar" style="background:{color};">{initial}</div>
                        <div class="review-meta">
                            <span class="review-name">{review["name"]}</span>
                            <span class="review-date">{review["date"]}</span>
                        </div>
                    </div>
                    <span class="review-stars">{stars}</span>
                    <p class="review-text">«{review["text"]}»</p>
                </div>
                """,
                unsafe_allow_html=True
                )

        st.write("")
        st.markdown('<hr class="section-divider">', unsafe_allow_html=True)