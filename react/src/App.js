import React,{ useEffect,useState } from 'react';
import './App.css';
import SearchIcon from './search.svg';
import MovieCard from './MovieCard';


const API_URL = `${process.env.REACT_APP_API_URL}/search`;
const API_URL2 = `${process.env.REACT_APP_API_URL}/movies`

const App = () =>{

    const [movie, setMovie] = useState([]);

    const [search, setSearch] =useState('');

    const searchItems = (searchValue) => {
        setSearch(searchValue)
        console.log(searchValue);
    }
    
    const searchMovies = async (title) => {
        console.log(`${API_URL}/${title}`);
        //alert(`${API_URL}/${title}`);
        const response = await fetch(`${API_URL}/${title}`);
        //alert(response);
        const data = await response.json();
        console.log(data);

        setMovie(Array.from(data));
        console.log(data.Search);
        
        console.log(movie);
    }
    const searchMovies2 = async (title) => {
        console.log(`${API_URL2}/${title}`);
        //alert(`${API_URL}/${title}`);
        const response = await fetch(`${API_URL2}/${title}`);
        //alert(response);
        const data = await response.json();
        console.log(data);

        setMovie(Array.from(data));
        console.log(data.Search);
        
        console.log(movie);
    }
    useEffect(() =>{
     searchMovies2('popular100');
    },[]);
    return(
        <div className='app'>
        <h1>MOVIEDB</h1>
        <div id='button-container'>
        <div className='inner'>
            <button onClick={()=>searchMovies2('top250')}> Top 250 </button>
        </div>
        <div className='inner'>
            <button onClick={()=>searchMovies2('popular100')}> Popular 100 </button>
        </div>
        <div className='inner'>
            <button onClick={()=>searchMovies2('bottom100')}> Bottom 100 </button>
        </div>
        <div className='inner'>
            <button onClick={()=>searchMovies2('ind250')}> Ind 250 </button>
        </div>
        <div className='inner'>
            <button onClick={()=>searchMovies2('toptv')}> Top TV </button>
        </div>
        </div>
        <div className='search'>
            <input type="text" placeholder="Search" onChange={(e)=> searchItems(e.target.value)} />
            <button onClick={()=>searchMovies(search)}><img src={SearchIcon}/></button>
        </div>
        <div className='container'>
        {Array.isArray(movie) ? (
            movie.map((data1) => {
            return(
                <div className='movie'>
                <MovieCard 
                    key={data1.title}
                    title={data1.title}
                    poster={data1.url}
                    year={data1.year}
                    rating={data1.rating}
                />
                </div>
            )
        })) : (
                <p>No movies found.</p>
        )}
        </div>
        </div>
    );
}

export default App;