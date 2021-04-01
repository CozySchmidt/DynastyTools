import './vote.scss';
import React, { Component } from "react";
import Typography from '@material-ui/core/Typography';
import axios from 'axios';
import { NEXT_MATCHUP, INSERT_MATCHUP } from '../../constants/api-urls';
import CircularProgress from '@material-ui/core/CircularProgress';
import VoteButton from '../votebutton/votebutton';
import Autocomplete from '@material-ui/lab/Autocomplete'
import TextField from '@material-ui/core/TextField';
import withStyles from "@material-ui/core/styles/withStyles";

const CustomAutocomplete = withStyles((theme) =>  ({
    inputRoot: {
        color: 'white',
        '&::before': {
            borderBottom: `1px solid white`
        },
        '&:hover:not(.Mui-disabled):before': {
            borderBottom: `2px solid white`
        }
    },
    popper: {
        backgroundColor: theme.palette.primary.light,
        borderBottomLeftRadius: '5px',
        borderBottomRightRadius: '5px'
    },
    listbox: {
        color: 'white',
        backgroundColor: theme.palette.primary.light
    },
    paper: {
        backgroundColor: theme.palette.primary.light,
        borderRadius: 0,
        boxShadow: 'none'
    },
    root: {
        '& .MuiFormLabel-root:not(.Mui-focused)': {
            color: 'white'
        }
    },
    popupIndicator: {
        color: 'white'
    }
}))(Autocomplete);


class Vote extends Component {

    constructor(props) {
        super(props);
        this.state = {
            error: null,
            response: null,
            submitting: false,
            position: "QB"
        }
    }

    componentDidMount() {
        this.nextMatchUp();
    }

    nextMatchUp = () => {
        let error, response;

        axios.post(NEXT_MATCHUP, {position: this.state.position}).then(res => {
            response = res;
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

        this.setState({submitting: true});
        
        axios.post(INSERT_MATCHUP, data).then(() => {
            this.nextMatchUp();
        }).catch(err => {
            console.log(err.message)
        })
    }

    updatePosition = (event, value) => {
        this.setState({position: value.id}, () => {
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
                        <CustomAutocomplete
                            options={POSITIONS}
                            style={{ width: 300 }}
                            blurOnSelect
                            disableClearable={true}
                            getOptionLabel={(option) => option.text}
                            renderInput={(params) => <TextField 
                                                        {...params}
                                                        label="Select Position" 
                                                        color="secondary" 
                                                    />
                                        }
                            onChange={this.updatePosition }
                            value={POSITIONS.find(position => position.id === this.state.position)}
                        >
                        </CustomAutocomplete>
                        
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

const POSITIONS = [
    {text: 'Quarterback', id: 'QB'},
    {text: 'Running Back', id: 'RB'},
    {text: 'Wide Receiver', id: 'WR'},
    {text: 'Tight End', id: 'TE'}
]

export default Vote;