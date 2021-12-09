import axios from 'axios';
import { useCallback, useEffect, useState } from 'react';
import { NEXT_MATCHUP, INSERT_MATCHUP } from '../constants/api-urls';
import PlayerCard from '../components/PlayerCard';
import ButtonGroup from "../components/ButtonGroup";
import { ThumbsUp } from 'react-feather';

//Router stuff
import { useSearchParams } from 'react-router-dom';

const VotePage = () => {
    const [searchParams, setSearchParams] = useSearchParams();

    const [error, setError] = useState();
    const [matchUp, setMatchUp] = useState(null);
    const [pos, setPos] = useState(searchParams.get('position'));
    const [submitting, setSubmitting] = useState();

    const POSITION_BUTTONS = [{label: 'All', value: 'All'}, 
                                {label: 'QB', value: 'QB'},
                                {label: 'RB', value: 'RB'},
                                {label: 'WR', value: 'WR'},
                                {label: 'TE', value: 'TE'}];

    const nextMatchUp = useCallback(() => {
        axios.get(`${NEXT_MATCHUP}${pos ? `?position=${pos}` :''}`).then(res => {
            setMatchUp(res.data);
            setSubmitting(false);
        }).catch(() => {
            setError('Oops! It looks like we\'re having trouble creating match ups. Please try again later.');
            setSubmitting(false);
        });

    }, [pos]);

    
    useEffect(() => {
        nextMatchUp();
    }, [pos, nextMatchUp])

    useEffect(() => {
        setPos(searchParams.get('position'));
    }, [searchParams])

    const submitVote = (winner) => {
        if (submitting) return;

        let data = {...matchUp};
        data.Winner = winner;

        setSubmitting(true);
        
        axios.post(INSERT_MATCHUP, data).then(() => {
            nextMatchUp();
        });
    }

    return (
        <section className="vote-section">
            <h1>Vote</h1>
            <p>Cast your vote below!</p>

            <div className="vote-wrapper">
                
                <ButtonGroup 
                    buttons={POSITION_BUTTONS} 
                    defaultValue="All" 
                    onChange={(pos) => setSearchParams({...searchParams, position: pos})} 
                    label="Choose A Position" 
                    value={pos ? pos : 'All'}
                />

                {
                    (error && ( <h2>{error}</h2> )) 
                    || (matchUp && ( 
                        <>
                            <button 
                                className={`vote-button`} 
                                aria-label={`Cast your vote for ${matchUp.PlayerOne.Name}`}
                                onClick={() => submitVote(matchUp.PlayerOne)}
                                disabled={submitting}>
                                <PlayerCard player={matchUp.PlayerOne} >
                                    <ThumbsUp className="vote-icon" />
                                </PlayerCard>
                            </button>
                            <button 
                                className={`vote-button`} 
                                aria-label={`Cast your vote for ${matchUp.PlayerTwo.Name}`}
                                onClick={() => submitVote(matchUp.PlayerTwo)}
                                disabled={submitting}>
                                <PlayerCard player={matchUp.PlayerTwo}  >
                                    <ThumbsUp className="vote-icon" />
                                </PlayerCard>
                            </button>
                        </>))
                    || ( <div id="matchup-loader">
                            loading...
                        </div> )
                }
            </div>
        </section>
    )
}

export default VotePage;