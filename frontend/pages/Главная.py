import streamlit as st


st.set_page_config(
    page_title="FILMS",
    page_icon="FILMS",
    layout="wide"
)



# подключение стилей

with open(
    "style.css",
    encoding="utf-8"
) as file:

    st.markdown(
        f"<style>{file.read()}</style>",
        unsafe_allow_html=True
    )



# главный экран


st.markdown(
"""

<div class="hero">


<div class="hero-content">


<h1>
ФИЛЬМЫ, КОТОРЫЕ<br>
МЕНЯЮТ РЕАЛЬНОСТЬ
</h1>


<p>
Истории, которые остаются в памяти навсегда
</p>


</div>


</div>


""",

unsafe_allow_html=True
)