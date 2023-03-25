from flask import Flask, request
import imdb, json

app = Flask(__name__)

ia = imdb.IMDb()
TOP_250 = 0
BOTTOM_100 = 1
POPULAR_100 = 2
TOP_250_INDIAN = 3
TOP_TV = 4 

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

def getMovieList(type):
    if type == TOP_250:
        return ia.get_top250_movies()
    elif type == BOTTOM_100:
        return ia.get_bottom100_movies()
    elif type == POPULAR_100:
        return ia.get_popular100_movies()
    elif type == TOP_250_INDIAN:
        return ia.get_top250_indian_movies()
    elif type == TOP_TV:
        return ia.get_top250_tv()
    
    return None


def getJsonMovie(moviestr):
    results = ia.search_movie(moviestr)
    movie_id = results[0].getID()
    movie = ia.get_movie(movie_id)

    return getMovieDict(movie)

def getMovie(moviestr):
    results = ia.search_movie(moviestr)
    movie_id = results[0].getID()
    movie = ia.get_movie(movie_id)

    return movie

def getJsonMovieList(list,rating):
    movie_list = []
    for movie in list:
        movie_dict = getTopDict(movie)
        if rating == '' or movie_dict['rating'] >= float(rating):
            movie_list.append(movie_dict)

    return json.dumps(movie_list, indent=4, separators=(',', ':'))



def getPopularMovies():
    return getJsonMovieList(getMovieList(POPULAR_100),'')


def getTop250():
    return getTop250('')

def getTop250(rating):
    return getJsonMovieList(getMovieList(TOP_250),rating)


def getBottom100():
    return getJsonMovieList(getMovieList(BOTTOM_100),'')

def getTop250Indian():
    return getJsonMovieList(getMovieList(TOP_250_INDIAN),'')

def getTopTV():
    return getJsonMovieList(getMovieList(TOP_TV),'')


@app.route("/")
def home():
    return ('Welcome to my favorite movies list!')

@app.route("/movies/<movie>" , methods=['GET'])
def get(movie):
    # movie_name = request.args.get('movie')
    movie_dict = getJsonMovie(movie)
    return json.dumps(movie_dict, indent=4, separators=(',', ':'))

@app.route("/rating/<rating>", methods=['GET'])
def get_rating(rating):
    return getTop250(rating)

@app.route("/movies/cast" , methods=['GET'])
def cast():
    movie_name = request.args.get('movie')
    rating_dict = getJsonMovie(movie_name)
    return json.dumps(rating_dict, indent=4, separators=(',', ':'))

@app.route("/movies/popular100", methods=['GET'])
def top():
    return getPopularMovies()

@app.route("/movies/top250", methods=['GET'])
def top250():
    return getTop250('')

@app.route("/movies/bottom100", methods=['GET'])
def bottom100():
    return getBottom100()

@app.route("/movies/ind250", methods=['GET'])
def indian250():
    return getTop250Indian()

@app.route("/movies/toptv", methods=['GET'])
def top250TV():
    return getTopTV()


if __name__ == '__main__':
    app.run(debug=True)
