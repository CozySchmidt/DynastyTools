import React, { Component } from "react";
import { Typography } from '@material-ui/core';
import Person from '@material-ui/icons/Person';
import ThumbUp from '@material-ui/icons/ThumbUp';
import './votebutton.scss';
import { withStyles } from "@material-ui/core/styles";
import PropTypes from 'prop-types';
import ButtonBase from '@material-ui/core/ButtonBase';

const themeStyles = theme => ({
    rippleVisible: {
        opacity: 0.1,
        color: '#6dfc35'
    }
})

class VoteButton extends Component {

    render() {
        const { classes } = this.props;
        
        return (
            <ButtonBase 
                    TouchRippleProps={{ classes: {root: classes.rippleVisible}}} 
                    className={`vote-button-container ${this.props.className}`}
                    onClick={this.props.onClick}
            >
                <Typography className={`player-name`} variant="h6">{this.props.player.Name ? this.props.player.Name : 'Player Name Unkown'}</Typography>
                <div className="player-pic-wrapper">
                    <Person className="player-pic"></Person>
                </div>
                <div className={`thumb-icon-wrapper`}>
                    <ThumbUp className="thumb-icon"></ThumbUp>
                </div>
            </ButtonBase>
        )
    }
}

VoteButton.propTypes = {
    classes: PropTypes.object.isRequired
}

export default withStyles(themeStyles)(VoteButton);