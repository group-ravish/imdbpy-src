from flask import Flask, request
import imdb, json

app = Flask(__name__)

ia = imdb.IMDb()

def getMovieDict(movie):

    movie_dict = {
        'title': movie.get('title'),
        'year': movie.get('year'),
        'rating': movie.get('rating'),
        'plot outline': movie.get('plot outline'),
        'genres': movie.get('genres'),
        'cast': [actor.get('name') for actor in movie.get('cast')],
        'directors': [director.get('name') for director in movie.get('directors')],
        'writers': [writer.get('name') for writer in movie.get('writers')]
    }

    return movie_dict

def getTopDict(movie):

    pop_dict = {
        'title': movie.get('title'),
        'year': movie.get('year'),
        'rating': movie.get('rating')
    }

    return pop_dict

def getRating(movie):

    rating_dict = {
        'rating': movie.get('rating'),
        'cast': [actor.get('name') for actor in movie.get('cast')[:3]],
    }   

    return rating_dict



def getJsonMovie(moviestr):
    results = ia.search_movie(moviestr)
    movie_id = results[0].getID()
    movie = ia.get_movie(movie_id)

    return getMovieDict(movie)


def getPopularMovies():
    pop = ia.get_popular100_movies()

    pop_list = []
    for movie in pop:
        pop_dict = getTopDict(movie)
        pop_list.append(pop_dict)

    return json.dumps(pop_list, indent=4, separators=(',', ':'))


def getTop250():
    top = ia.get_top250_movies()

    top_mov = []
    for movie in top:
        top_dict = getTopDict(movie)
        top_mov.append(top_dict)
    
    return json.dumps(top_mov, indent=4, separators=(',', ':'))


def getActorRating(moviestr):
    movies = ia.search_movie(moviestr)
    movie = movies[0]
    ia.update(movie)

    return getRating(movie)


@app.route("/")
def home():
    return ('Welcome to my favorite movies list!')

@app.route("/movies" , methods=['GET'])
def get():
    movie_name = request.args.get('movie')
    movie_dict = getJsonMovie(movie_name)
    return json.dumps(movie_dict, indent=4, separators=(',', ':'))

@app.route("/movies/popular100", methods=['GET'])
def top():
    return getPopularMovies()

@app.route("/movies/top250", methods=['GET'])
def top250():
    return getTop250()

@app.route("/movies/cast" , methods=['GET'])
def cast():
    movie_name = request.args.get('movie')
    rating_dict = getJsonMovie(movie_name)
    return json.dumps(rating_dict, indent=4, separators=(',', ':'))


if __name__ == '__main__':
    app.run(debug=True)