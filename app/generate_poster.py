import requests

API_KEY = '54a3f35e89c5e2709f8ecbf1eedba06c'
AUTH_TOKEN = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI1NGEzZjM1ZTg5YzVlMjcwOWY4ZWNiZjFlZWRiYTA2YyIsIm5iZiI6MTc3MzMyMDQ2Ny45MTkwMDAxLCJzdWIiOiI2OWIyYjkxMzQ4YjUyNDljYmY0YjZmYmYiLCJzY29wZXMiOlsiYXBpX3JlYWQiXSwidmVyc2lvbiI6MX0.ED801PxjJCn1oLKNZllqZyR367StbWjRzwOitoq4t88"

HEADERS = {'Authorization': f'Bearer {AUTH_TOKEN}'}
BASE_URL = 'https://api.themoviedb.org/3'
POSTER_BASE_URL = 'https://image.tmdb.org/t/p/w300'

def get_poster_url(movie_title):
    response = requests.get(
        f'{BASE_URL}/search/movie',
        headers=HEADERS,
        params={'query': movie_title},
        timeout=10
    )
    results = response.json().get('results')
    if not results:
        return None
    return POSTER_BASE_URL + results[0]['poster_path']