import React, { Component } from "react";
import AppBar from '@material-ui/core/AppBar';
import Tabs from '@material-ui/core/Tabs';
import Tab from '@material-ui/core/Tab';
import { Toolbar, Typography } from "@material-ui/core";
import './navbar.scss';
import Vote from '../vote/vote';
import Rankings from "../rankings/rankings";
import Calculator from "../calculator/calculator";
import { NavLink } from "react-router-dom";

export const HIDDEN = {
    VOTE: 0,
    RANKINGS: 1,
    CALCULATOR: 2
}

class Navbar extends Component {

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
                            <Tab label="Vote">
                                <NavLink exact to="/"></NavLink>
                            </Tab>
                            <Tab label="Rankings">
                                <NavLink exact to="/rankings"></NavLink>
                            </Tab>
                            <Tab label="Calculator">
                                <NavLink exact to="/calculator"></NavLink>
                            </Tab>
                        </Tabs>
                        <Typography id="tabs-heading" variant="h5">
                            Consensus Rankings
                        </Typography>
                    </Toolbar>
                
                </AppBar>

            </div>
        );
    }

    handleChange = (event, newValue) => {
        this.setState({value: newValue})
    }
}

export default Navbar;