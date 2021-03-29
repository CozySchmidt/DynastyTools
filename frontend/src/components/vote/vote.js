import './vote.scss';
import React, { Component } from "react";
import { Typography } from '@material-ui/core';
import axios from 'axios';
import { NEXT_MATCHUP, INSERT_MATCHUP } from '../../constants/api-urls';
import CircularProgress from '@material-ui/core/CircularProgress';
import VoteButton from '../votebutton/votebutton'

class Vote extends Component {

    constructor(props) {
        super(props);
        this.state = {
            error: null,
            response: null
        }
    }

    componentDidMount() {
        this.nextMatchUp();
    }

    nextMatchUp = () => {
        axios.post(NEXT_MATCHUP, {position: 'QB'}).then(res => {
            this.setState({response: res})
        }).catch(err => {
            this.setState({error: err})
        })
    }

    submitVote(winner) {
        let data = this.state.response.data;
        data.Winner = winner
        console.log(data);
        
        axios.post(INSERT_MATCHUP, data).then(res => {
            this.nextMatchUp();
        }).catch(err => {
            console.log(err.message)
        })
    }

    /**
     * Returns the inner html for the vote container depending on the current state
     * 
     * @returns 
     */
    getInnerContents() {
        if (this.state.error) {
            return (
                <Typography variant="h5">
                    Error: {this.state.error.message}
                </Typography>
            );
        } else if (this.state.response !== null) {
            return (
                <div id="matchup-container">
                    <div id="vote-button-container">
                        <VoteButton 
                            className="vote-button" 
                            player={this.state.response.data.PlayerOne}
                            onClick={() => this.submitVote(this.state.response.data.PlayerOne)}
                        >
                        </VoteButton>
                        <VoteButton 
                            className="vote-button" 
                            player={this.state.response.data.PlayerTwo}
                            onClick={() => this.submitVote(this.state.response.data.PlayerTwo)}
                        >
                        </VoteButton>
                    </div>
                </div>
            );
        }

        return LOADING
    }

    render() {
        let view = (
            <div id="vote-container">
                {this.getInnerContents()}
            </div>
        );

        return view;
    }
}

const LOADING = <div id="matchup-loader"><CircularProgress className="loading-bar"/></div>

export default Vote;