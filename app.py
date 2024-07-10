import streamlit as st
import pickle
import numpy as np
import pandas as pd
import requests


# Function to get movie poster from TMDb
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=d1370240dce2c7ead96bb953e0276ad7&language=en-US"
    response = requests.get(url)
    data = response.json()
    if 'poster_path' in data:
        poster_path = data['poster_path']
        full_path = f"https://image.tmdb.org/t/p/w500{poster_path}"
        return full_path
    return None


# Function to get movie ID from TMDb
def get_movie_id(movie_title):
    url = f"https://api.themoviedb.org/3/search/movie?api_key=d1370240dce2c7ead96bb953e0276ad7&query={movie_title}"
    response = requests.get(url)
    data = response.json()
    if 'results' in data and len(data['results']) > 0:
        return data['results'][0]['id']
    return None


def recommend(movie):
    index = np.where(movies["title"] == movie)[0][0]
    similar_movies = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])[1:6]

    recommend_movies = []
    recommend_posters = []
    for i in similar_movies:
        movie_title = movies["title"][i[0]]
        recommend_movies.append(movie_title)

        movie_id = get_movie_id(movie_title)
        if movie_id:
            poster_url = fetch_poster(movie_id)
            recommend_posters.append(poster_url if poster_url else "Poster not available")
        else:
            recommend_posters.append("Poster not available")

    return recommend_movies, recommend_posters


# Load your data
movies = pickle.load(open("movies.pkl", "rb"))
similarity = pickle.load(open('similarity.pkl', 'rb'))
movies_list = movies["title"].values

st.title("Movie Recommender System")

option = st.selectbox("Movies", movies_list)

if st.button("Recommend"):
    recommendations, posters = recommend(option)
    cols = st.columns(5)  # Create 5 columns for the 5 recommendations
    for col, title, poster in zip(cols, recommendations, posters):
        with col:
            st.text(title)
            if poster != "Poster not available":
                st.image(poster, width=125)
            else:
                st.text(poster)
