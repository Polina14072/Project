import streamlit as st
import os
from utils import load_css, render_nav


st.set_page_config(
    page_title="FILMS | Топ",
    layout="wide"
)


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
load_css(BASE_DIR, os.path.join("..", "style.css"))

render_nav("Топ")


st.markdown(
"""
<div class="movies-title">
<h1>10 ФИЛЬМОВ, КОТОРЫЕ СТОИТ ПОСМОТРЕТЬ</h1>
<p>Подборка атмосферных фильмов и сериалов</p>
</div>
""",
unsafe_allow_html=True
)


top_movies = [

{
"name": "Дьявол носит Prada",
"genre": "Драма, комедия",
"imdb": 6.9,
"wiki": "https://ru.wikipedia.org/wiki/Дьявол_носит_Prada"
},

{
"name": "Марсианин",
"genre": "Фантастика, приключения",
"imdb": 8.0,
"wiki": "https://ru.wikipedia.org/wiki/Марсианин_(фильм)"
},

{
"name": "Король Ричард",
"genre": "Драма, спорт",
"imdb": 7.5,
"wiki": "https://ru.wikipedia.org/wiki/Король_Ричард"
},

{
"name": "Жизнь Чака",
"genre": "Драма, фантастика",
"imdb": 7.2,
"wiki": "https://ru.wikipedia.org/wiki/Жизнь_Чака"
},

{
"name": "Чёрная пантера",
"genre": "Фантастика, боевик",
"imdb": 7.3,
"wiki": "https://ru.wikipedia.org/wiki/Чёрная_пантера_(фильм,_2018)"
},

{
"name": "Интерстеллар",
"genre": "Фантастика, драма",
"imdb": 8.7,
"wiki": "https://ru.wikipedia.org/wiki/Интерстеллар"
},

{
"name": "Первому игроку приготовиться",
"genre": "Фантастика, приключения",
"imdb": 7.4,
"wiki": "https://ru.wikipedia.org/wiki/Первому_игроку_приготовиться_(фильм)"
},

{
"name": "Гарри Поттер",
"genre": "Фэнтези, приключения",
"imdb": 7.6,
"wiki": "https://ru.wikipedia.org/wiki/Гарри_Поттер_и_философский_камень_(фильм)"
},

{
"name": "Энола Холмс",
"genre": "Детектив, приключения",
"imdb": 6.6,
"wiki": "https://ru.wikipedia.org/wiki/Энола_Холмс"
},

{
"name": "Дюна",
"genre": "Фантастика, драма",
"imdb": 8.0,
"wiki": "https://ru.wikipedia.org/wiki/Дюна_(фильм,_2021)"
},

]


for index, movie in enumerate(top_movies, start=1):


    number = str(index).zfill(2)


    st.markdown(
    f"""
    <div class="top-item">
    <span class="top-number">{number}</span>
    <h2>{movie["name"]}</h2>
    <p class="top-genre">{movie["genre"]}</p>
    <p class="top-imdb">
    IMDb: {movie["imdb"]}
    <a href="{movie["wiki"]}" target="_blank">Подробнее →</a>
    </p>
    </div>
    """,
    unsafe_allow_html=True
    )


    st.write("---")