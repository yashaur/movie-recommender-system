import streamlit as st
import pandas as pd
from app.recommender import get_recommendations, indices
from app.generate_poster import get_poster_url

st.set_page_config(page_title="Movie Recommender", layout="wide")

st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=DM+Sans:wght@300;400;500&display=swap');
 
        html, body, [class*="css"] {
            font-family: 'DM Sans', sans-serif;
            background-color: #0e0e0e;
            color: #f0f0f0;
        }
        .title {
            font-family: 'DM Serif Display', serif;
            font-size: 3rem;
            color: #f0f0f0;
            margin-bottom: 0;
        }
        .subtitle {
            color: #888;
            font-size: 1rem;
            margin-bottom: 2.5rem;
        }
        .stButton > button {
            background-color: #f0f0f0;
            color: #0e0e0e;
            font-family: 'DM Sans', sans-serif;
            font-weight: 500;
            border: none;
            border-radius: 8px;
            padding: 0.6rem 2rem;
            width: 100%;
            transition: opacity 0.2s;
        }
        .stButton > button:hover { opacity: 0.85; }
        .movie-title {
            font-size: 0.85rem;
            color: #ccc;
            text-align: center;
            margin-top: 0.4rem;
            line-height: 1.3;
        }
        .section-label {
            font-family: 'DM Serif Display', serif;
            font-size: 1.4rem;
            margin-bottom: 1rem;
            color: #f0f0f0;
        }
        hr { border-color: #222; margin: 2rem 0; }
 
        @keyframes fadeScale {
            from { opacity: 0; transform: scale(0.9); }
            to   { opacity: 1; transform: scale(1); }
        }
 
        [data-testid="stImage"] img {
            animation: fadeScale 0.5s ease forwards;
            opacity: 0;
        }
 
        [data-testid="stImage"]:nth-child(1) img { animation-delay: 0.0s; }
        [data-testid="stImage"]:nth-child(2) img { animation-delay: 0.1s; }
        [data-testid="stImage"]:nth-child(3) img { animation-delay: 0.2s; }
        [data-testid="stImage"]:nth-child(4) img { animation-delay: 0.3s; }
        [data-testid="stImage"]:nth-child(5) img { animation-delay: 0.4s; }
        [data-testid="stImage"]:nth-child(6) img { animation-delay: 0.5s; }
        [data-testid="stImage"]:nth-child(7) img { animation-delay: 0.6s; }
        [data-testid="stImage"]:nth-child(8) img { animation-delay: 0.7s; }
        [data-testid="stImage"]:nth-child(9) img { animation-delay: 0.8s; }
        [data-testid="stImage"]:nth-child(10) img { animation-delay: 0.9s; }
    </style>
""", unsafe_allow_html=True)


# --- Header ---
st.markdown('<p class="title">Cinescope</p>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Enter three films you love. We\'ll find your next favourite.</p>', unsafe_allow_html=True)

# --- Inputs ---
valid_titles = indices.index.tolist()

col1, col2, col3 = st.columns(3)
with col1:
    movie1 = st.selectbox("First movie", options=[""] + valid_titles, index=0)
with col2:
    movie2 = st.selectbox("Second movie", options=[""] + valid_titles, index=0)
with col3:
    movie3 = st.selectbox("Third movie", options=[""] + valid_titles, index=0)

_, btn_col, _ = st.columns([2, 1, 2])
with btn_col:
    submitted = st.button("Find Recommendations")

# --- Recommendations ---
if submitted:
    titles = [movie1, movie2, movie3]
    missing = [t for t in titles if not t.strip()]
    if missing:
        st.warning("Please enter all three movie titles.")
    else:
        with st.spinner("Finding recommendations..."):
            try:
                recommendations = get_recommendations(
                    movie_titles=titles
                )
                st.markdown("<hr>", unsafe_allow_html=True)
                st.markdown('<p class="section-label">Recommended for you</p>', unsafe_allow_html=True)

                cols = st.columns(5)
                for i, title in enumerate(recommendations):
                    with cols[i % 5]:
                        poster_url = get_poster_url(title)
                        if poster_url:
                            st.image(poster_url, use_container_width=True)
                        else:
                            st.image("https://via.placeholder.com/300x450?text=No+Poster", use_container_width=True)
                        st.markdown(f'<p class="movie-title">{title}</p>', unsafe_allow_html=True)

            except KeyError as e:
                st.error(f"Movie not found in dataset: {e}. Please check the title and try again.")