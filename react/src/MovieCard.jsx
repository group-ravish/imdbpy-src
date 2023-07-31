import React from'react'
const MovieCard = (props) => {
    return(
        <>
            <h2>{props.title}</h2>
            <img src={props.poster} class="center"/>
            <h2>{props.year}</h2>
            <h2>{props.rating}</h2>
            
        </>
    )
};

export default MovieCard;