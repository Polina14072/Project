markdown("<h2>О фильме</h2>", unsafe_allow_html=True)

    st.write(movie["plot"])

    st.markdown(
    f"""
    <p><b>Жанр:</b> {movie["genre"]}</p>
    <p><b>Год:</b> {movie["year"]}</p>
    <p><b>Режиссёр:</b> {movie["director"]}</p>
    <p><b>Рейтинг:</b> {movie["rating"]} / 10</p>
    """,
    unsafe_allow_html=True
    )


    st.write("---")


    st.markdown("<h2>АКТЁРЫ</h2>", unsafe_allow_html=True)

    cols = st.columns(len(movie["actors"]))

    for col, actor in zip(cols, movie["actors"]):

        with col:

            render_image(actor["image"], "actor-photo")

            st.markdown(
            f"""
            <h3 class="actor-name">{actor["name"]}</h3>
            <p class="actor-role">{actor["role"]}</p>
            """,
            unsafe_allow_html=True
            )


    st.write("---")


    st.markdown("<h2>ТРЕЙЛЕР</h2>", unsafe_allow_html=True)

    st.markdown(
    f"""
    <div class="trailer-wrapper">
        <iframe src="{movie["trailer"]}"
                frameborder="0"
                allow="clipboard-write; autoplay"
                allowfullscreen
                webkitAllowFullScreen
                mozallowfullscreen>
        </iframe>
    </div>
    """,
    unsafe_allow_html=True
    )