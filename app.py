import pickle
import streamlit as st
import requests


def fetch_movie_details(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    data = requests.get(url).json()

    poster_path = data.get('poster_path')
    rating = data.get('vote_average')
    release_year = data.get('release_date', '')[:4] if data.get('release_date') else 'N/A'

    full_poster_path = f"https://image.tmdb.org/t/p/w500/{poster_path}" if poster_path else "https://via.placeholder.com/500x750?text=No+Image"

    return full_poster_path, rating, release_year


def recommend(movie):
    if movie not in movies['title'].values:
        return [], [], [], []

    index = movies[movies['title'] == movie].index[0]
    distances = sorted(enumerate(similarity[index]), reverse=True, key=lambda x: x[1])

    recommended_movie_names = []
    recommended_movie_posters = []
    movie_ratings = []
    movie_years = []

    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        poster, rating, year = fetch_movie_details(movie_id)

        recommended_movie_names.append(movies.iloc[i[0]].title)
        recommended_movie_posters.append(poster)
        movie_ratings.append(rating)
        movie_years.append(year)

    return recommended_movie_names, recommended_movie_posters, movie_ratings, movie_years


st.header('🎬 Movie Recommender System')

# Load data
movies = pickle.load(open('movie_list.pkl', 'rb'))
similarity = pickle.load(open('similarity.pkl', 'rb'))

movie_list = movies['title'].values
selected_movie = st.selectbox("🎥 Type or select a movie from the dropdown", movie_list)

if st.button('🔍 Show Recommendations'):
    recommended_movie_names, recommended_movie_posters, movie_ratings, movie_years = recommend(selected_movie)

    if recommended_movie_names:
        col1, col2, col3, col4, col5 = st.columns(5)

        with col1:
            st.text(recommended_movie_names[0])
            st.image(recommended_movie_posters[0])
            st.caption(f"Rating: {movie_ratings[0]}/10")
            st.caption(f"Year: {movie_years[0]}")

        with col2:
            st.text(recommended_movie_names[1])
            st.image(recommended_movie_posters[1])
            st.caption(f"Rating: {movie_ratings[1]}/10")
            st.caption(f"Year: {movie_years[1]}")

        with col3:
            st.text(recommended_movie_names[2])
            st.image(recommended_movie_posters[2])
            st.caption(f"Rating: {movie_ratings[2]}/10")
            st.caption(f"Year: {movie_years[2]}")

        with col4:
            st.text(recommended_movie_names[3])
            st.image(recommended_movie_posters[3])
            st.caption(f"Rating: {movie_ratings[3]}/10")
            st.caption(f"Year: {movie_years[3]}")

        with col5:
            st.text(recommended_movie_names[4])
            st.image(recommended_movie_posters[4])
            st.caption(f"Rating: {movie_ratings[4]}/10")
            st.caption(f"Year: {movie_years[4]}")
    else:
        st.write("Movie not found in database!")