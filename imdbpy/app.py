from flask import Flask, request
import imdb, json
import logging
from flask_cors import CORS

logger = logging.getLogger('imdblogger')
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.FileHandler('app.log'))

app = Flask(__name__)
CORS(app)

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
        'directors': getDirectorList(movie),
        'writers': [writer.get('name') for writer in movie.get('writers')]
    }

    return movie_dict

def getDirectorList(movie):
    directorNames = []
    if movie.get('directors') == None:
        return directorNames
    for director in movie.get('directors'):
        directorNames.append(director.get('name'))

    return directorNames

def getTopDict(movie):

    pop_dict = {
        'title': movie.get('title'),
        'year': movie.get('year'),
        'rating': movie.get('rating'),
        'url': movie.get('cover url')
    }

    return pop_dict


def getMovieList(type):
    if type == TOP_250:
        top250 = ia.search_movie_advanced('matrix', results = 100)
        logger.debug('TOP250: %s', top250)
        return top250
    elif type == BOTTOM_100:
        bottom100 = ia.search_movie_advanced('avengers', results = 100)
        logger.debug('BOTTOM100: %s', bottom100)
        return bottom100
    elif type == POPULAR_100:
        pop100 = ia.search_movie_advanced('america', results = 100)
        logger.debug('POPULAR100: %s', pop100)
        return pop100
    elif type == TOP_250_INDIAN:
        ind250 = ia.search_movie_advanced('love', results = 100)
        logger.debug('IND250: %s', ind250)
        return ind250
    elif type == TOP_TV:
        toptv = ia.search_movie_advanced('man', results = 100)
        logger.debug('TOPTV: %s', toptv)
        return toptv
    return None


def getJsonMovie(moviestr):

    results = ia.search_movie(moviestr)
    movie_id = results[0].getID()
    movie = ia.get_movie(movie_id)

    return getTopDict(movie)

def getMovie(moviestr):
    movie_list = []
    movie = ia.search_movie_advanced(moviestr, results = 100)
    # length = len(results)
    for i in movie:
        # movie_id = results[i].getID()
        # movie = ia.get_movie(movie_id)
        movie_list.append(getTopDict(i))
    return movie_list

def getJsonMovieList(list,rating):
    movie_list = []
    logger.info('The list and rating are: ', list, rating)
    for movie in list:
        movie_dict = getTopDict(movie)
        logger.info('Movie Dict is: ', movie_dict)
        if rating == '' or movie_dict['rating'] >= float(rating):
            movie_list.append(movie_dict)
            logger.info('Movie List is: ', movie_list)

    return json.dumps(movie_list, indent=4, separators=(',', ':'))

def setLogLevel(loglevel):
    loglevel = loglevel.lower()
    if loglevel == 'debug':
        response = 'Log level set to DEBUG'
        logger.setLevel(logging.DEBUG)
        return response
    elif loglevel == 'info':
        response = 'Log level set to INFO'
        logger.setLevel(logging.INFO)
        return response
    elif loglevel == 'warning':
        response = 'Log level set to WARNING'
        logger.setLevel(logging.WARNING)
        return response
    elif loglevel == 'error':
        response = 'Log level set to ERROR'
        logger.setLevel(logging.ERROR)
        return response
    elif loglevel == 'critical':
        response = 'Log level set to CRITICAL'
        logger.setLevel(logging.CRITICAL)
        return response
    else:
        response = 'Unsupported log level! Defaulting to INFO level!'
        logger.error(response)
        logger.setLevel(logging.INFO)
        return response



def getPopularMovies(rating):
    return getJsonMovieList(getMovieList(POPULAR_100),rating)

def getTop250():
    return getTop250('')

def getTop250(rating):
    return getJsonMovieList(getMovieList(TOP_250),rating)

def getBottom100(rating):
    return getJsonMovieList(getMovieList(BOTTOM_100),rating)

def getTop250Indian(rating):
    return getJsonMovieList(getMovieList(TOP_250_INDIAN),rating)

def getTopTV(rating):
    return getJsonMovieList(getMovieList(TOP_TV),rating)


@app.route("/")
def home():
    return ('Welcome to our MovieDB!')

@app.route("/loglevel/<loglevel>", methods=['GET'])
def log(loglevel):
    return setLogLevel(loglevel)

@app.route("/search/<movie>" , methods=['GET'])
def search(movie):
    # movie_name = request.args.get('movie')
    movie_dict = getMovie(movie)
    return json.dumps(movie_dict, indent=4, separators=(',', ':'))
    # return searchMovie('')

@app.route("/rating/top250/<rating>", methods=['GET'])
def get_rating(rating):
    return getTop250(rating)

@app.route("/rating/pop100/<rating>", methods=['GET'])
def get_pop_rating(rating):
    return getPopularMovies(rating)

@app.route("/rating/ind250/<rating>", methods=['GET'])
def get_ind_rating(rating):
    return getTop250Indian(rating)

@app.route("/rating/toptv/<rating>", methods=['GET'])
def get_tv_rating(rating):
    return getTopTV(rating)

@app.route("/movies/cast" , methods=['GET'])
def cast():
    movie_name = request.args.get('movie')
    rating_dict = getJsonMovie(movie_name)
    return json.dumps(rating_dict, indent=4, separators=(',', ':'))

@app.route("/movies/popular100", methods=['GET'])
def top():
    return getPopularMovies('')

@app.route("/movies/top250", methods=['GET'])
def top250():
    return getTop250('')

@app.route("/movies/bottom100", methods=['GET'])
def bottom100():
    return getBottom100('')

@app.route("/movies/ind250", methods=['GET'])
def indian250():
    return getTop250Indian('')

@app.route("/movies/toptv", methods=['GET'])
def top250TV():
    return getTopTV('')


if __name__ == '__main__':
    app.run(debug=True)
