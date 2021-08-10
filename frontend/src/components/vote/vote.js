import './vote.scss';
import React, { Component } from "react";
import Typography from '@material-ui/core/Typography';
import axios from 'axios';
import { NEXT_MATCHUP, INSERT_MATCHUP } from '../../constants/api-urls';
import CircularProgress from '@material-ui/core/CircularProgress';
import VoteButton from '../votebutton/votebutton';
import { ButtonGroupBox } from '../../materialstyles/buttongroupbox';
import { CustomToggleButton } from '../../materialstyles/customtogglebutton';
import { CustomToggleButtonGroup } from '../../materialstyles/customtogglebuttongroup';

class Vote extends Component {

    constructor(props) {
        super(props);
        this.state = {
            error: null,
            response: null,
            submitting: false,
            position: "All"
        }
    }

    componentDidMount() {
        this.nextMatchUp();
    }

    nextMatchUp = () => {
        let error, response;
        axios.get(NEXT_MATCHUP+'?position='+this.state.position, {headers:{"X-CSRFToken": CSRF_TOKEN}}).then(res => {
            response = res;
            console.log(response);
        }).catch(err => {
            error = err;
        }).then(() => {
            if (this.isUnmounted) return;
            this.setState({error: error, response: response, submitting: false});
        })
    }

    submitVote(winner) {
        if (this.state.submitting) return;

        let data = this.state.response.data;
        data.Winner = winner;
        console.log(data);
        this.setState({submitting: true});
        
        axios.post(INSERT_MATCHUP, data, {headers:{"X-CSRFToken": CSRF_TOKEN}}).then(() => {
            this.nextMatchUp();
        }).catch(err => {
            console.log(err.message)
        })
    }

    updatePosition = (event, value) => {
        if (!value) return;

        this.setState({position: value}, () => {
            this.nextMatchUp();
        });
    }

    componentWillUnmount() {
        this.isUnmounted = true;
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
        } else if (this.state.response) {
            return (
                <div id="matchup-container">
                    <div id="vote-options">
                        <ButtonGroupBox className="vote-option">
                            <Typography variant="body1">Position</Typography>
                            <CustomToggleButtonGroup 
                                size="medium"
                                value={this.state.position}
                                aria-label="Select Position"
                                onChange={this.updatePosition}
                                exclusive 
                            >
                                {POSITIONS.map((pos) => (
                                    <CustomToggleButton value={pos} key={pos} aria-label={pos + " selector button"}>
                                        <Typography variant="body2">{pos}</Typography>
                                    </CustomToggleButton>
                                ))}
                            </CustomToggleButtonGroup>
                        </ButtonGroupBox>
                    </div>
                    <div id="vote-button-container">
                        <div className="vote-button" >
                            <VoteButton 
                                player={this.state.response.data.PlayerOne}
                                onClick={() => this.submitVote(this.state.response.data.PlayerOne)}
                            >
                            </VoteButton>
                        </div>
                        <div className="vote-button">
                            <VoteButton 
                                player={this.state.response.data.PlayerTwo}
                                onClick={() => this.submitVote(this.state.response.data.PlayerTwo)}
                            >
                            </VoteButton>
                        </div>
                    </div>
                </div>
            );

        }

        return (
            <div id="matchup-loader">
                <CircularProgress className="loading-bar" color="secondary"/>
            </div>
        );
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

const CSRF_TOKEN = document.cookie ? document.cookie.split('; ')?.find(row => row.startsWith('csrftoken='))?.split('=')[1] : null;

const POSITIONS = ['All', 'QB', 'RB', 'WR', 'TE'];

export default Vote;