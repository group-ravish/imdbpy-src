from flask import Flask, request
import imdb, json

app = Flask(__name__)

ia = imdb.IMDb()

def getMovieDict(movie):
    print(movie)

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

    print(movie_dict)
    return movie_dict

def getjsonmovie(moviestr):
    results = ia.search_movie(moviestr)
    movie_id = results[0].getID()
    movie = ia.get_movie(movie_id)

    return getMovieDict(movie)

def getPopularMovies():
    pop = ia.get_popular100_movies()
    pop_list = []

    for movie in pop:
        print(movie)
        movie_dict = getMovieDict(movie)
        print(movie_dict)
        pop_list.append(movie_dict)

    return json.dumps(pop_list)



@app.route("/")
def home():
    return ('Welcome to my favorite movies list!')

@app.route("/movies" , methods=['GET'])
def get():
    movie_name = request.args.get('movie')
    movie_dict = getjsonmovie(movie_name)
    return json.dumps(movie_dict)

@app.route("/movies/popular100", methods=['GET'])
def top():
    return getPopularMovies()


if __name__ == '__main__':
    app.run(debug=True)
