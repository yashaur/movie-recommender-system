import joblib
import pandas as pd
import numpy as np
from sklearn.preprocessing import normalize

indices = joblib.load('./artifacts/indices.pkl')
cosine_sim = joblib.load('./artifacts/cosine_sim.pkl')

def get_recommendations(movie_titles):
    
    sim_scores = []
    input_movie_indices = []

    for title in movie_titles:
        idx = indices.loc[title, 'index']
        input_movie_indices.append(idx)
        sim_scores.append(cosine_sim[idx])

    weights = [1, 1, 1]

    sim_scores = np.average(np.array(sim_scores), axis = 0, weights = weights)
    
    sim_scores = enumerate(normalize(sim_scores.reshape(1,-1), norm='l2').flatten())

    sim_scores = sorted(sim_scores, key = lambda x: x[1], reverse = True)

    movie_indices = [i[0] for i in sim_scores if i[0] not in input_movie_indices][:10]

    # return movie_indices

    return indices.iloc[movie_indices].reset_index()['title']

if __name__ == '__main__':

    test_movies = [
                    'The Big Short',
                    'The Godfather',
                    'Spider-Man',
    ]

    recos = get_recommendations(test_movies)

    print(recos)