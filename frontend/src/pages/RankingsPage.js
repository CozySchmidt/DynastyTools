import { useCallback, useEffect, useState } from "react";
import axios from 'axios';
import { GET_RANKINGS } from '../constants/api-urls';
import ButtonGroup from "../components/ButtonGroup";
import PlayerCard from "../components/PlayerCard";

//Router stuff
import { useSearchParams } from 'react-router-dom';
import { withRouter } from '../hooks/withRouter';
import { Grid, List } from "react-feather";

const RankingsPage = () => {
    const [searchParams, setSearchParams] = useSearchParams();

    const [error, setError] = useState(null);
    const [pos, setPos] = useState(searchParams.get('position'));
    const [players, setPlayers] = useState();
    const [layout, setLayout] = useState('list');

    const POSITION_BUTTONS = [{label: 'All', value: 'All'}, 
                                {label: 'QB', value: 'QB'},
                                {label: 'RB', value: 'RB'},
                                {label: 'WR', value: 'WR'},
                                {label: 'TE', value: 'TE'}];

    const LAYOUT_BUTTONS = [
        {label: (<List />), value: 'list'},
        {label: (<Grid />), value: 'grid'}
    ]


    const getRankings = useCallback(() => {
        axios.get(`${GET_RANKINGS}${pos ? `?position=${pos}` :''}`).then(res => {
            setPlayers(res.data);
        }).catch(() => {
            setError('Oops! It looks like we\'re having trouble gathering the rankings. Please try again later.');
        });
    }, [pos]);

    useEffect(() => {
        if (pos) setSearchParams({...searchParams, position: pos});

        getRankings();
    }, [pos, getRankings, searchParams, setSearchParams])

    return (
        <section className={`rankings-section`}>
            <h1>Rankings</h1>
            <p className="caption">Ranking {pos ? pos : 'All'} Players</p>

            <div className="filters">
                <ButtonGroup 
                    buttons={POSITION_BUTTONS} 
                    defaultValue="All" 
                    onChange={setPos} 
                    label="Select A Position" 
                    value={pos}
                />
            </div>

            <ButtonGroup 
                buttons={LAYOUT_BUTTONS} 
                defaultValue="list" 
                onChange={setLayout}
                className="layout-btn-group"
            />

            {
                (error && ( <h2>{error}</h2>)) 
                ||
                (players &&
                    (layout === 'grid' ?
                    <div className={`players-wrapper ${layout}`}>
                        { players.map((player, i) => <PlayerCard player={player} showFullDetails key={player.id} animateOnChange={false} placement={i + 1}/>) }
                    </div> :
                    <div className="table-wrapper">
                        <table className="players-table">
                            <thead>
                                <tr>
                                    <th>#</th>
                                    <th>Name</th>
                                    <th>Rating</th>
                                    <th>Position</th>
                                    <th>Age</th>
                                    <th>Drafted</th>
                                </tr>
                            </thead>
                            <tbody>
                                { players.map((player, i) => (
                                    <tr>
                                        <td>{i + 1}</td>
                                        <td>{player.Name}</td>
                                        <td>{player.Rating.toFixed(0)}</td>
                                        <td>{player.Position}</td>
                                        <td>{player.Age.toFixed(0)}</td>
                                        <td>{player.Draftyear}</td>
                                    </tr>
                                )) }
                            </tbody>
                        </table>
                    </div>)
                ) 
                || 
                <div id="matchup-loader">
                    <p>Loading...</p>
                </div>
            }
        </section>
    )
}

export default withRouter(RankingsPage);