import './vote.scss';
import React, { Component } from "react";
import { Typography } from '@material-ui/core';
import { AxiosProvider, Request, Get, Delete, Head, Post, Put, Patch, withAxios } from 'react-axios';
import { NEXT_MATCHUP } from '../../constants/api-urls';

class Vote extends Component {
    
    render() {
        return (
            <div id="vote-container">
                <Get url={NEXT_MATCHUP} params={{position: "QB"}}>
                    {(error, response, isLoading, makeRequest, axios) => {
                        if(error) {
                            return (
                                <Typography variant="h5">
                                    Error: {error.message}
                                </Typography>
                            );
                        } else if (response !== null) {
                            return (
                                <Typography variant="h5">
                                    {response.data.PlayerOneName} VS {response.data.PlayerTwoName} 
                                </Typography>
                            );
                        } else if (isLoading) {
                            return <p>Loading</p>
                        }

                        return <p>Default Message</p>
                    }}
                </Get>
                
            </div>
        );
    }
}

export default Vote;