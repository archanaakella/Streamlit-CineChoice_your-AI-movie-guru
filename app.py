import pickle
import streamlit as st
import pandas as pd
import requests

# Function to fetch movie posters from TMDB API
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=6457bb89e3d30f9dd6388259a2eece13"
    data = requests.get(url).json()
    
    if 'poster_path' in data and data['poster_path']:  # Ensure poster exists
        return f"https://image.tmdb.org/t/p/w500/{data['poster_path']}"
    return "https://via.placeholder.com/500x750?text=No+Image"

# Load the pickled model data
try:
    with open(r"C:\Users\archa\Downloads\Movie Recommendation System\model\movie_dict.pkl", "rb") as f:
        movies = pickle.load(f)
    with open(r"C:\Users\archa\Downloads\Movie Recommendation System\model\similarity.pkl", "rb") as f:
        similarity = pickle.load(f)
except FileNotFoundError:
    st.error("Model files not found! Please ensure 'movie_list.pkl' and 'similarity.pkl' are in the 'model' directory.")
    st.stop()

# Ensure movies is a DataFrame
if isinstance(movies, dict):  
    movies = pd.DataFrame(movies)

# Clean title column
movies["title"] = movies["title"].astype(str).str.strip()

# Movie Recommendation Function
def recommend(movie):
    if movie not in movies["title"].values:
        return [], []
    
    index = movies[movies["title"] == movie].index[0]
    distances = sorted(enumerate(similarity[index]), key=lambda x: x[1], reverse=True)
    
    recommended_movie_names = []
    recommended_movie_posters = []
    
    for i in distances[1:6]:  # Top 5 similar movies
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_names.append(movies.iloc[i[0]].title)
        recommended_movie_posters.append(fetch_poster(movie_id))
    
    return recommended_movie_names, recommended_movie_posters

# Streamlit UI
st.title("🎬 Movie Recommendation System")

# Dropdown for selecting a movie
movie_list = movies["title"].values
selected_movie = st.selectbox("Select a movie:", movie_list)

# Show recommendations
if st.button("Show Recommendations"):
    recommended_names, recommended_posters = recommend(selected_movie)
    
    if recommended_names:
        cols = st.columns(5)  # Display in 5 columns
        for i, col in enumerate(cols):
            with col:
                st.text(recommended_names[i])
                st.image(recommended_posters[i])
    else:
        st.warning("No recommendations found!")













