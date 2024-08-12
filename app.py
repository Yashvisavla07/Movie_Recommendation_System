import streamlit as st
import pickle
import pandas as pd
import requests

st.title('Movie Recommender System')


def recommend(movie):
    movies_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movies_index]
    movies_list = sorted(list(enumerate(distances)) , reverse = True , key = lambda x:x[1])[1:6]

    recommend_movies = []
    recommended_movies_posters = []
    for i in movies_list:
        movies_id = movies.iloc[i[0]].movie_id
        recommend_movies.append(movies.iloc[i[0]].title)

        # fetch poster from API
        recommended_movies_posters.append(fetch_poster(movies_id))

    return recommend_movies , recommended_movies_posters

def fetch_poster(movies_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}?api_key=87072c1579792d947f1013e2ef25efec'.format(movies_id))
    data = response.json()
    return "https://image.tmdb.org/t/p/w500" + data['poster_path']

similarity =  pickle.load(open('similarity.pkl' , 'rb'))

movies_dict = pickle.load(open('movies.pkl' , 'rb'))
movies = pd.DataFrame(movies_dict)

print(movies)

selected_movies_list = st.selectbox(
"How would you like to be contacted?",
movies['title'].values)

if st.button("Recommend"):
    names , posters = recommend(selected_movies_list)

    col1, col2, col3, col4, col5 = st.columns(5)

    with col1:
       st.text(names[0])
       st.image(posters[0])

    with col2:
       st.text(names[1])
       st.image(posters[1])

    with col3:
       st.text(names[2])
       st.image(posters[2])

    with col4:
       st.text(names[3])
       st.image(posters[3])

    with col5:
       st.text(names[4])
       st.image(posters[4])