import React, { Component } from "react";
import AppBar from '@material-ui/core/AppBar';
import Tabs from '@material-ui/core/Tabs';
import Tab from '@material-ui/core/Tab';
import { Toolbar, Typography } from "@material-ui/core";
import './tabs.scss';
import Vote from '../vote/vote';
import Rankings from "../rankings/rankings";
import Calculator from "../calculator/calculator";

export const HIDDEN = {
    VOTE: 0,
    RANKINGS: 1,
    CALCULATOR: 2
}

class Nav extends Component {

    constructor(props) {
        super(props);
        this.state = {
            value: 0
        }
    }

    render() {

        return (
            <div id="mat-tabs">
                <AppBar position="static" elevation={0}>
                    <Toolbar id="tabs-toolbar">
                        <Tabs 
                            value={this.state.value} 
                            onChange={this.handleChange} 
                            aria-label="page tabs"
                            id="tabs"
                        >
                            <Tab label="Vote" />
                            <Tab label="Rankings" />
                            <Tab label="Calculator" />
                        </Tabs>
                        <Typography id="tabs-heading" variant="h5">
                            Consensus Rankings
                        </Typography>
                    </Toolbar>
                
                </AppBar>
                <div role="tabpanel" className="tab-panel" hidden={this.state.value !== HIDDEN.VOTE}>
                    <Vote></Vote>
                </div>
                
                <div role="tabpanel" className="tab-panel"  hidden={this.state.value !== HIDDEN.RANKINGS}>
                    <Rankings></Rankings>
                </div> 

                <div role="tabpanel" className="tab-panel"  hidden={this.state.value !== HIDDEN.CALCULATOR}>
                    <Calculator></Calculator>
                </div> 
            </div>
        );
    }

    handleChange = (event, newValue) => {
        this.setState({value: newValue})
    }
}

export default Nav;