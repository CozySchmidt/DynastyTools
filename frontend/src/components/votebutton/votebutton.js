import React, { Component } from "react";
import Typography from '@material-ui/core/Typography';
import Person from '@material-ui/icons/Person';
import ThumbUp from '@material-ui/icons/ThumbUp';
import './votebutton.scss';
import ButtonBase from '@material-ui/core/ButtonBase';
import Slide from '@material-ui/core/Slide';

class VoteButton extends Component {

    constructor(props) {
        super(props);

        this.state = {
            playerData: this.props.player,
            animate: false
        }
    }

    componentDidUpdate(prevProps) {
        if (prevProps.player !== this.props.player) {
            this.setState({animate: true})
        }
    }

    onAnimationEnd = () => {
        this.setState({animate: false, playerData: this.props.player})
    }

    render() {
        
        return (
            <ButtonBase 
                className={`vote-button-container ${this.state.playerData.Team}`}
                onClick={this.state.animate ? null : this.props.onClick}
            >
                <Slide 
                    direction={this.state.animate ? "up" : "down"}
                    in={!this.state.animate} 
                    onExited={this.onAnimationEnd}
                    timeout={{enter: 400, exit: 300}}
                >
                    <div className={`vote-button-contents`}>
                        <Typography className={`player-name`} variant="h6">{this.state.playerData.Name ? this.state.playerData.Name : 'Name Unkown'}</Typography>
                        <Typography className={`player-team`} variant="subtitle1">{this.state.playerData.Team ? this.state.playerData.Team : 'Team Unkown'}</Typography>
                        <div className="player-pic-wrapper">
                            <Person className="player-pic"></Person>
                        </div>
                        <div className={`thumb-icon-wrapper`}>
                            <ThumbUp className="thumb-icon"></ThumbUp>
                        </div>
                    </div>
                </Slide>
            </ButtonBase>
        )
    }
}

export default VoteButton;