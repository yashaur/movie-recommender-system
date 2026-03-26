import requests
from io import BytesIO
from PIL import Image

FALLBACK_POSTER_PATH = './artifacts/movie_poster_not_found.jpg'

def get_poster_url(movie_title):

    API_KEY = '46f52586'
    BASE_URL = 'http://www.omdbapi.com'
    POSTER_BASE_URL = 'http://img.omdbapi.com'

    try:
        # Try exact title match first, fall back to search
        try:
            params_omdb = {'t': movie_title, 'apikey': API_KEY}
            response = requests.get(BASE_URL, params=params_omdb).json()
        except:
            params_omdb = {'s': movie_title, 'apikey': API_KEY}
            response = requests.get(BASE_URL, params=params_omdb).json()['Search'][0]

        id = response['imdbID']
        imdb_poster_url = response['Poster']

        # Try OMDB poster API first, fall back to IMDB poster URL
        try:
            params_poster = {'i': id, 'h': 350, 'apikey': API_KEY}
            poster = Image.open(BytesIO(requests.get(POSTER_BASE_URL, params=params_poster).content))
        except:
            poster = Image.open(BytesIO(requests.get(imdb_poster_url).content))

        return poster

    except Exception as e:
        print(f"Could not fetch poster for '{movie_title}': {e}")
        return Image.open(FALLBACK_POSTER_PATH)