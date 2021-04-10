import './rankings.scss';
import React, { Component } from "react";
import Typography from '@material-ui/core/Typography';
import axios from 'axios';
import { GET_RANKINGS } from '../../constants/api-urls';
import CircularProgress from '@material-ui/core/CircularProgress';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableContainer from '@material-ui/core/TableContainer';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import withStyles from "@material-ui/core/styles/withStyles";
import { ButtonGroupBox } from '../../materialstyles/buttongroupbox';
import { CustomToggleButton } from '../../materialstyles/customtogglebutton';
import { CustomToggleButtonGroup } from '../../materialstyles/customtogglebuttongroup';

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
        axios.post(GET_RANKINGS, {position: this.state.position}, {headers:{"X-CSRFToken": CSRF_TOKEN}}).then(res => {
            this.tableData = this.setState({tableData: res.data});
            this.setTeams();
        }).catch(err => {
            console.log(err)
        })
    }

    updatePosition = (event, value) => {
        if (!value) return;

        this.setState({position: value}, () => {
            this.getRankings();
        });
    }

    setTeams = () => {
        let newTeams = [];
        this.setState({teams: newTeams});
        this.setState({filteredTeams: []});

        for (let i = 0; i < this.state.tableData.length; i++) {
            if (!this.state.teams.find(team => team === this.state.tableData[i].Team)) {
                newTeams.push(this.state.tableData[i].Team);
            }
        }

        newTeams.sort();

        this.setState({teams: newTeams});
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
                        <ButtonGroupBox className="ranking-filter">
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

                        <ButtonGroupBox className="ranking-filter">
                            <Typography variant="body1">Scoring</Typography>
                            <CustomToggleButtonGroup 
                                size="medium"
                                value={this.state.position}
                                aria-label="Select Scoring Type"
                                exclusive 
                            >
                                {SCORING.map((scoring) => (
                                    <CustomToggleButton value={scoring} key={scoring} aria-label={scoring + " selector button"}>
                                        <Typography variant="body2">{scoring}</Typography>
                                    </CustomToggleButton>
                                ))}
                            </CustomToggleButtonGroup>
                        </ButtonGroupBox>

                        <ButtonGroupBox className="ranking-filter">
                            <Typography variant="body1">Teams</Typography>
                            <CustomToggleButtonGroup 
                                size="medium"
                                value={this.state.filteredTeams}
                                aria-label="Select Teams"
                                onChange={this.setFilteredTeams }
                            >
                                {this.state.teams.map((team) => (
                                    <CustomToggleButton value={team} key={team} aria-label={team + " selector"}>
                                        <Typography variant="body2">{team}</Typography>
                                    </CustomToggleButton>
                                ))}
                            </CustomToggleButtonGroup>
                        </ButtonGroupBox>
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

                                    return null;
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

const CSRF_TOKEN = document.cookie.split('; ').find(row => row.startsWith('csrftoken=')).split('=')[1];

const SCORING = ['Std', 'Half-PPR', 'PPR'];

const POSITIONS = ['QB', 'RB', 'WR', 'TE'];

export default Rankings;