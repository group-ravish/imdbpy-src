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
        'rating': movie.get('rating')
    }

    return pop_dict


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

    return getTopDict(movie)

def getMovie(moviestr):
    movie_list = []
    results = ia.search_movie(moviestr)
    length = len(results)
    for i in range(length-1):
        movie_id = results[i].getID()
        #print('RESULT OF I: ', results[i])
        #movie = ia.get_movie(movie_id)
        movie_list.append(getTopDict(results[i]))
        print (results[i])
    return movie_list

def getJsonMovieList(list,rating):
    movie_list = []
    for movie in list:
        movie_dict = getTopDict(movie)
        if rating == '' or movie_dict['rating'] >= float(rating):
            movie_list.append(movie_dict)

    return json.dumps(movie_list, indent=4, separators=(',', ':'))



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
    return ('Welcome to my favorite movies list!')

@app.route("/movies/<movie>" , methods=['GET'])
def get(movie):
    # movie_name = request.args.get('movie')
    movie_dict = getMovie(movie)
    return json.dumps(movie_dict, indent=4, separators=(',', ':'))

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
