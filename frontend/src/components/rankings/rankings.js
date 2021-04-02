import './rankings.scss';
import React, { Component } from "react";
import Typography from '@material-ui/core/Typography';
import axios from 'axios';
import { GET_RANKINGS } from '../../constants/api-urls';
import CircularProgress from '@material-ui/core/CircularProgress';
import Autocomplete from '@material-ui/lab/Autocomplete'
import TextField from '@material-ui/core/TextField';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableContainer from '@material-ui/core/TableContainer';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
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
    tag: {
        backgroundColor: theme.palette.secondary.dark,
        color: theme.palette.common.white
    },
    popper: {
        backgroundColor: theme.palette.primary.light,
        borderBottomLeftRadius: '5px',
        borderBottomRightRadius: '5px',
        boxShadow: '0 2px 8px 1px rgba(0, 0, 0, 0.25)'
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

const CustomTableCell = withStyles((theme) => ({
    head: {
      backgroundColor: theme.palette.primary.light,
      color: theme.palette.common.white,
    },
    body: {
        backgroundColor: theme.palette.primary.light,
        color: theme.palette.common.white,
    },
    root: {
        borderBottom: '1px solid rgba(255, 255, 255, 0.2)'
    },
}))(TableCell);

const CustomTableContainer = withStyles((theme) => ({
    root: {
        boxShadow: '0 0 5px rgba(0, 0, 0, 0.25)'
    }
}))(TableContainer)

class Rankings extends Component {

    constructor(props) {
        super(props);
        this.state = {
            error: null,
            position: "QB",
            tableData: null,
            teams: [],
            filteredTeams: []
        }
    }

    componentDidMount() {
        this.getRankings();
    }

    getRankings = () => {
        axios.post(GET_RANKINGS, {position: this.state.position}).then(res => {
            this.tableData = this.setState({tableData: res.data});
            this.setTeams();
        }).catch(err => {
            console.log(err)
        })
    }

    updatePosition = (event, value) => {
        this.setState({position: value.id}, () => {
            this.getRankings();
        });
    }

    setTeams = () => {
        this.setState({teams: []});

        for (let i = 0; i < this.state.tableData.length; i++) {
            if (!this.state.teams.find(team => team === this.state.tableData[i].Team)) {
                this.state.teams.push(this.state.tableData[i].Team)
            }
        }
    }

    setFilteredTeams = (event, value) => {
        this.setState({filteredTeams: value});
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
        } else if (this.state.tableData) {
            return (
                <div id="ranking-wrapper">
                    <div id="ranking-filters">
                        <CustomAutocomplete
                            className="ranking-filter"
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
                        <CustomAutocomplete
                            multiple
                            size="small"
                            limitTags={this.state.teams.length - 1}
                            className="ranking-filter"
                            options={this.state.teams}
                            style={{ width: 300 }}
                            blurOnSelect
                            disableClearable={true}
                            getOptionLabel={(option) => option}
                            renderInput={(params) => <TextField 
                                                        {...params}
                                                        label="Filter Teams" 
                                                        color="secondary" 
                                                    />
                                        }
                            onChange={this.setFilteredTeams }
                        >
                        </CustomAutocomplete>
                    </div>
                    <CustomTableContainer className="rankings-table">
                        <Table>
                            <TableHead>
                                <TableRow>
                                    <CustomTableCell><Typography variant="subtitle1">Rating</Typography></CustomTableCell>
                                    <CustomTableCell><Typography variant="subtitle1">Name</Typography></CustomTableCell>
                                    <CustomTableCell><Typography variant="subtitle1">Team</Typography></CustomTableCell>
                                </TableRow>
                            </TableHead>
                            <TableBody>
                                {this.state.tableData.map((row) => {
                                    if (this.state.filteredTeams.find(team => team === row.Team) || this.state.filteredTeams.length === 0) {
                                        return (
                                            <TableRow key={row.Name}>
                                                <CustomTableCell>{row.Rating}</CustomTableCell>
                                                <CustomTableCell>{row.Name}</CustomTableCell>
                                                <CustomTableCell>{row.Team}</CustomTableCell>
                                            </TableRow>
                                        )
                                    }
                                })}
                            </TableBody>
                        </Table>
                    </CustomTableContainer>
                    
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
            <div id="rankings-container">
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

export default Rankings;