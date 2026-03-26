from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import numpy as np
from sklearn.preprocessing import normalize
import joblib
import pandas as pd
from api.generate_poster import get_poster_url
import base64, io
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

app = FastAPI(title = 'Movie Recommender')

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

indices = joblib.load('./artifacts/indices.pkl')
cosine_sim = joblib.load('./artifacts/cosine_sim.pkl')

class Movie_input(BaseModel):
    titles: list[str]

class Recommendation_output(BaseModel):
    recommendations: list

class MovieListOutput(BaseModel):
    titles: list[str]

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

    recos = indices.iloc[movie_indices].drop(columns = 'index').reset_index(names = 'title').T.to_dict()
    recos = [recos[n] for n in range(10)]
    
    for idx, movie in enumerate([movie['title'] for movie in recos]):
        poster_img = get_poster_url(movie)
        if poster_img:
            buf = io.BytesIO()
            poster_img.save(buf, format="JPEG")
            poster_img = base64.b64encode(buf.getvalue()).decode()
        else:
            with open('./artifacts/movie_poster_not_found.jpg', 'rb') as f:
                poster_img = base64.b64encode(f.read()).decode()
        
        recos[idx]['poster'] = poster_img

    return recos

@app.get("/")
async def serve_frontend():
    return FileResponse("app.html")

@app.get('/titles', response_model = MovieListOutput)
async def get_titles():
    return {'titles': indices.index.to_list()}


@app.post('/recommend', response_model = Recommendation_output)
async def recommend(payload: Movie_input):

    movie_titles = payload.titles
    recos = get_recommendations(movie_titles=movie_titles)

    return {'recommendations': recos}

@app.get("/health")
def health_check():
    return {"status": "ok"}