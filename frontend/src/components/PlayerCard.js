import { useEffect, useRef, useState } from "react";
import { User } from "react-feather";

const PlayerCard = ({ player, showFullDetails, children, animateOnChange = true, placement }) => {
    
    const cardRef = useRef();
    const [playerToShow, setPlayerToShow] = useState(player);

    useEffect(() => {
        if (!animateOnChange) setPlayerToShow(player)
    }, [player, animateOnChange]);

    return (
        <article className={`player-card ${playerToShow.Team}`} ref={cardRef} >
            <div className="main-details-wrapper">
                <div 
                    className={`main-details ${animateOnChange && (playerToShow === player ? 'enter' : 'exit')}`} 
                    onAnimationEnd={() => setPlayerToShow(player)}
                >
                    <h3>{placement ? `${placement}. `: ''}{playerToShow.Name ? playerToShow.Name : 'Name Unkown'}</h3>
                    <h4>{playerToShow.Team ? playerToShow.Team : 'Team Unkown'}</h4>
                    <div className="player-pic-wrapper">
                        <User className="player-pic" />
                    </div>

                    
                    {children}
                </div>
            </div>

            
            {showFullDetails && (<div className="other-details">
                <p>Rating: {playerToShow.Rating.toFixed(0)}</p>
                <p>Position: {playerToShow.Position}</p>
                <p>Drafted: {playerToShow.Draftyear}</p>
                <p>Age: {playerToShow.Age.toFixed(0)}</p>
            </div>)}
        </article>
    )
}

export default PlayerCard;