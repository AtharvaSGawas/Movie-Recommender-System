import streamlit as st
import pickle
import pandas as pd
import requests

# IMDB-style Dark Theme CSS with Enhanced Elements
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&family=Oswald:wght@400;500;600&display=swap');
    
    /* Main background - IMDB dark theme */
    .stApp {
        background: #0f0f0f;
        color: #ffffff;
        font-family: 'Roboto', sans-serif;
    }
    
    /* Title styling - IMDB yellow accent */
    .main-title {
        text-align: center;
        font-family: 'Oswald', sans-serif;
        font-size: 4rem;
        font-weight: 600;
        color: #f5c518;
        text-shadow: 2px 2px 8px rgba(245, 197, 24, 0.3);
        margin-bottom: 1rem;
        animation: fadeInDown 1s ease-out;
        letter-spacing: 2px;
    }
    
    .subtitle {
        text-align: center;
        font-size: 1.3rem;
        color: #d4d4d4;
        margin-bottom: 3rem;
        animation: fadeInUp 1s ease-out 0.5s both;
        font-weight: 300;
    }
    
    /* Main container - Dark card style */
    .main-container {
        background: #1a1a1a;
        border-radius: 12px;
        padding: 2.5rem;
        margin: 2rem 0;
        box-shadow: 0 8px 32px rgba(0,0,0,0.6);
        border: 1px solid #333333;
    }
    
    /* Selectbox styling - IMDB style */
    .stSelectbox > div > div {
        background: #2a2a2a !important;
        border: 2px solid #404040 !important;
        border-radius: 8px !important;
        color: #ffffff !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.3) !important;
    }
    
    .stSelectbox > div > div:hover {
        border-color: #f5c518 !important;
    }
    
    .stSelectbox > div > div > div {
        color: #ffffff !important;
        background: #2a2a2a !important;
    }
    
    /* Button styling - IMDB yellow */
    .stButton > button {
        background: linear-gradient(135deg, #f5c518 0%, #e6b800 100%) !important;
        color: #000000 !important;
        border: none !important;
        border-radius: 8px !important;
        padding: 0.8rem 2.5rem !important;
        font-size: 1.1rem !important;
        font-weight: 500 !important;
        font-family: 'Oswald', sans-serif !important;
        box-shadow: 0 4px 15px rgba(245, 197, 24, 0.4) !important;
        transition: all 0.3s ease !important;
        width: 100% !important;
        text-transform: uppercase !important;
        letter-spacing: 1px !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 6px 20px rgba(245, 197, 24, 0.6) !important;
        background: linear-gradient(135deg, #ffdd44 0%, #f5c518 100%) !important;
    }
    
    /* Movie card styling - Dark cards with IMDB feel */
    .movie-card {
        background: #1f1f1f;
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 8px 25px rgba(0,0,0,0.4);
        transition: all 0.3s ease;
        margin: 0.5rem;
        animation: fadeInUp 0.6s ease-out;
        border: 1px solid #333333;
        min-height: 400px;
        display: flex;
        flex-direction: column;
        justify-content: space-between;
    }
    
    .movie-card:hover {
        transform: translateY(-8px);
        box-shadow: 0 15px 40px rgba(245, 197, 24, 0.2);
        border-color: #f5c518;
    }
    
    /* Loading placeholder styling */
    .movie-placeholder {
        background: linear-gradient(90deg, #2a2a2a 25%, #333333 50%, #2a2a2a 75%);
        background-size: 200% 100%;
        animation: shimmer 2s infinite;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 0.5rem;
        min-height: 400px;
        border: 1px solid #404040;
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }
    
    .placeholder-icon {
        font-size: 3rem;
        color: #555555;
        margin-bottom: 1rem;
        animation: pulse 2s infinite;
    }
    
    .placeholder-text {
        color: #888888;
        font-size: 0.9rem;
        text-align: center;
        font-style: italic;
        font-weight: 300;
    }
    
    /* Text styling for movie titles */
    .stText {
        color: #ffffff !important;
        font-weight: 500 !important;
        text-align: center !important;
        margin-bottom: 1rem !important;
        font-size: 1rem !important;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.7) !important;
        font-family: 'Roboto', sans-serif !important;
    }
    
    /* Image styling with IMDB poster feel */
    .stImage > img {
        border-radius: 8px !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 6px 20px rgba(0,0,0,0.5) !important;
        border: 1px solid #333333 !important;
        width: 100% !important;
        height: auto !important;
    }
    
    .stImage > img:hover {
        transform: scale(1.05) !important;
        box-shadow: 0 8px 30px rgba(245, 197, 24, 0.3) !important;
    }
    
    /* Header styling */
    .header-section {
        background: linear-gradient(135deg, #1a1a1a 0%, #2a2a2a 100%);
        padding: 2rem;
        border-radius: 12px;
        margin-bottom: 2rem;
        border: 1px solid #333333;
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
        position: relative;
        overflow: hidden;
    }
    
    .header-section::before {
        content: '';
        position: absolute;
        top: 0;
        left: -100%;
        width: 100%;
        height: 100%;
        background: linear-gradient(90deg, transparent, rgba(245, 197, 24, 0.1), transparent);
        animation: shine 3s infinite;
    }
    
    /* Stats section */
    .stats-section {
        background: #1a1a1a;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 1rem 0;
        border: 1px solid #333333;
        text-align: center;
    }
    
    .stat-item {
        display: inline-block;
        margin: 0 2rem;
        padding: 0.5rem;
    }
    
    .stat-number {
        display: block;
        font-size: 2rem;
        font-weight: 700;
        color: #f5c518;
        font-family: 'Oswald', sans-serif;
    }
    
    .stat-label {
        display: block;
        font-size: 0.9rem;
        color: #b3b3b3;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Footer styling - IMDB style */
    .footer {
        text-align: center;
        padding: 2.5rem;
        margin-top: 4rem;
        background: #1a1a1a;
        border-radius: 12px;
        border: 1px solid #333333;
        box-shadow: 0 4px 20px rgba(0,0,0,0.3);
    }
    
    .footer-text {
        color: #b3b3b3;
        font-size: 0.95rem;
        margin-bottom: 0.5rem;
        font-weight: 300;
    }
    
    .creator-name {
        color: #f5c518;
        font-weight: 500;
        font-size: 1.2rem;
        text-shadow: 1px 1px 3px rgba(0,0,0,0.7);
        font-family: 'Oswald', sans-serif;
    }
    
    .api-credit {
        color: #888888;
        font-size: 0.85rem;
        margin-top: 1rem;
        font-weight: 300;
        font-style: italic;
    }
    
    /* Rating-style accent */
    .imdb-accent {
        color: #f5c518;
        font-weight: 600;
    }
    
    /* Animations */
    @keyframes fadeInDown {
        from {
            opacity: 0;
            transform: translateY(-40px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(40px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes shimmer {
        0% {
            background-position: -200% 0;
        }
        100% {
            background-position: 200% 0;
        }
    }
    
    @keyframes pulse {
        0%, 100% {
            opacity: 0.5;
        }
        50% {
            opacity: 1;
        }
    }
    
    @keyframes shine {
        0% {
            left: -100%;
        }
        100% {
            left: 100%;
        }
    }
    
    /* Column spacing */
    .stColumn {
        padding: 0 0.5rem;
    }
    
    /* Custom scrollbar */
    ::-webkit-scrollbar {
        width: 8px;
    }
    
    ::-webkit-scrollbar-track {
        background: #1a1a1a;
    }
    
    ::-webkit-scrollbar-thumb {
        background: #f5c518;
        border-radius: 4px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: #ffdd44;
    }
    
    /* Hide streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* Override Streamlit defaults */
    .stApp > div:first-child {
        background: #0f0f0f;
    }
    
    /* Dropdown options styling */
    .stSelectbox > div > div > div > div {
        background: #2a2a2a !important;
        color: #ffffff !important;
    }
    
    /* Select box label */
    .stSelectbox > label {
        color: #f5c518 !important;
        font-weight: 500 !important;
        font-size: 1.1rem !important;
        margin-bottom: 0.5rem !important;
    }
    
    /* Recommendations header */
    .recommendations-header {
        text-align: center;
        color: #f5c518;
        font-family: 'Oswald', sans-serif;
        margin: 2rem 0;
        padding: 1rem;
        background: rgba(245, 197, 24, 0.1);
        border-radius: 8px;
        border: 1px solid rgba(245, 197, 24, 0.3);
    }
</style>
""", unsafe_allow_html=True)

def fetch_poster(movie_id):
    try:
        response = requests.get(f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=2e47a13aeb0d7023ec52632cfd1696cf&language=en-US')
        data = response.json()
        poster_path = data.get('poster_path')
        if poster_path:
            return f"https://image.tmdb.org/t/p/w500/{poster_path}"
        else:
            return "https://via.placeholder.com/500x750/333333/ffffff?text=No+Poster"
    except:
        return "https://via.placeholder.com/500x750/333333/ffffff?text=No+Poster"

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies = []
    recommended_movies_posters = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]]['id']
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_movies_posters

# Load data
movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# Header Section
st.markdown('<h1 class="main-title">🎬 CineMatch</h1>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Your Personal Movie Discovery Engine</p>', unsafe_allow_html=True)

# Movie Selection
st.markdown('<div class="main-container">', unsafe_allow_html=True)
movie_list = movies['title'].values
selected_movie = st.selectbox(
    "🔍 Search & Select a Movie",
    movie_list,
    help="Type to search or scroll to find your favorite movie"
)

# Initialize session state for recommendations
if 'show_recommendations' not in st.session_state:
    st.session_state.show_recommendations = False
    st.session_state.recommended_movies = []
    st.session_state.recommended_posters = []

if st.button('🎯 Get Recommendations'):
    with st.spinner('🎭 Finding perfect matches...'):
        recommended_movies, recommended_movies_posters = recommend(selected_movie)
        st.session_state.recommended_movies = recommended_movies
        st.session_state.recommended_posters = recommended_movies_posters
        st.session_state.show_recommendations = True

st.markdown('</div>', unsafe_allow_html=True)

# Show recommendations when button is clicked
if st.session_state.show_recommendations:
    st.markdown(f'<div class="recommendations-header"><h3>🌟 Movies Similar to "{selected_movie}" 🌟</h3></div>', unsafe_allow_html=True)
    
    col1, col2, col3, col4, col5 = st.columns(5)
    columns = [col1, col2, col3, col4, col5]
    
    for i, col in enumerate(columns):
        with col:
            st.markdown('<div class="movie-card">', unsafe_allow_html=True)
            st.markdown(f'<div class="stText">{st.session_state.recommended_movies[i]}</div>', unsafe_allow_html=True)
            st.image(st.session_state.recommended_posters[i], use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)

# Enhanced Footer
st.markdown("""
<div class="footer">
    <div class="footer-text">Crafted with <span class="imdb-accent">❤️</span> using Streamlit & Python</div>
    <div class="creator-name">Atharva Sunil Gawas</div>
    <div class="api-credit">
        Powered by The Movie Database (TMDb) API<br>
        <span class="imdb-accent">★</span> Delivering cinematic recommendations since 2024 <span class="imdb-accent">★</span>
    </div>
</div>
""", unsafe_allow_html=True)