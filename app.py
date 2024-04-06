import pickle
import streamlit as st
import requests

OMDB_API_KEY = "1d5d236"

def fetch_movie_details(movie_title):
    url = f"http://www.omdbapi.com/?t={movie_title}&apikey={OMDB_API_KEY}"
    data = requests.get(url)
    data = data.json()
    director = data['Director']
    rating = data['imdbRating']
    cast = data['Actors']
    release_year = data['Year']
    poster_url = data['Poster']
    return director, rating, cast, release_year, poster_url

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_directors = []
    recommended_movie_ratings = []
    recommended_movie_casts = []
    recommended_movie_years = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        # fetch the movie details
        movie_title = movies.iloc[i[0]].title
        director, rating, cast, release_year, poster_url = fetch_movie_details(movie_title)
        recommended_movie_names.append(movie_title)
        recommended_movie_directors.append(director)
        recommended_movie_ratings.append(rating)
        recommended_movie_casts.append(cast)
        recommended_movie_years.append(release_year)
        recommended_movie_posters.append(poster_url)

    return recommended_movie_names, recommended_movie_directors, recommended_movie_ratings, recommended_movie_casts, recommended_movie_years, recommended_movie_posters


st.header('Movie Recommender System Using Machine Learning')

directory_path = 'C:\\Users\\vimal\\My_projects\\recommendation\\antifacts'

movies = pickle.load(open(directory_path + '\\new_df.pkl','rb'))
similarity = pickle.load(open(directory_path + '\\similarity.pkl','rb'))

movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movie_list
)

if st.button('Show Recommendation'):
    recommended_movie_names, recommended_movie_directors, recommended_movie_ratings, recommended_movie_casts, recommended_movie_years, recommended_movie_posters = recommend(selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5)
    for i in range(5):
        with col1:
            st.text(recommended_movie_names[i])
            st.text(f"Director: {recommended_movie_directors[i]}")
            st.text(f"Rating: {recommended_movie_ratings[i]}")
            st.text(f"Cast: {recommended_movie_casts[i]}")
            st.text(f"Year: {recommended_movie_years[i]}")
            st.image(recommended_movie_posters[i])
