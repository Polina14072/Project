import streamlit as st
import os
import base64
import mimetypes


st.set_page_config(
    page_title="FILMS | Фильмы",
    layout="wide"
)


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSS_PATH = os.path.join(BASE_DIR, "..", "style.css")


with open(
    CSS_PATH,
    encoding="utf-8"
) as file:

    st.markdown(
        f"<style>{file.read()}</style>",
        unsafe_allow_html=True
    )



def get_image_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()



def get_mime_type(path):
    mime_type, _ = mimetypes.guess_type(path)
    return mime_type or "image/jpeg"



st.markdown(
"""
<div class="movies-title">
<h1>
Фильмы
</h1>
</div>
""",
unsafe_allow_html=True
)



movies = [


{
"name":"Аватар",
"image":"assets/avatar.jpeg"
},


{
"name":"Начало",
"image":"assets/inception.jpg"
},


{
"name":"Голодные игры",
"image":"assets/Hunger.webp"
}

]



for movie in movies:


    left, right = st.columns(
        [2,1]
    )


    with left:


        st.markdown(
        f"""
        <div class="film-info">

        <h2>
        {movie["name"]}
        </h2>

        </div>
        """,
        unsafe_allow_html=True
        )


        if st.button(
            "Подробнее",
            key=f"details_{movie['name']}"
        ):

            st.session_state["selected_movie"] = movie["name"]
            st.switch_page("pages/movie_details.py")



    with right:


        img_path = os.path.join(BASE_DIR, "..", movie["image"])


        if os.path.exists(img_path):

            img_base64 = get_image_base64(img_path)
            mime_type = get_mime_type(img_path)

            st.markdown(
            f"""
            <div class="film-poster">
                <img src="data:{mime_type};base64,{img_base64}">
            </div>
            """,
            unsafe_allow_html=True
            )

        else:

            st.error(f"Картинка не найдена: {img_path}")


    st.write("")