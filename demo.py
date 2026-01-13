import pandas as pd
import streamlit as st
import pickle
import requests

def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    data = requests.get(url).json()
    poster_path = data.get('poster_path')

    if poster_path:
        return "https://image.tmdb.org/t/p/w500/" + poster_path
    else:
        return None


movies = pickle.load(open('movie.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl','rb'))
new = movies

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]

    distances = sorted(
        list(enumerate(similarity[index])),
        reverse=True,
        key=lambda x: x[1]
    )

    recommended_movie = []
    recommended_posters = []

    for i in distances[1:6]:
        movie_row = movies.iloc[int(i[0])]
        recommended_movie.append(movie_row['title'])
        recommended_posters.append(
            fetch_poster(int(movie_row['movie_id']))
        )

    return recommended_movie, recommended_posters


st.title('Movie Recommendation System')
movie = st.selectbox(
    'How would you like to predict?',
    movies['title'].values)

if st.button('Recommend'):
    names, posters = recommend(movie)
    st.subheader('Recommended Movies')

    count =min(len(names), len(posters))
    cols=st.columns(count)

    for i  in range(count):
        with cols[i]:
            st.text(names[i])
            if posters[i]:
               st.image(posters[i])
            else:
                st.write('poster not available')