import React, { Component } from "react";
import { MuiThemeProvider, unstable_createMuiStrictModeTheme as createMuiTheme } from '@material-ui/core/styles';  
import Navbar from './components/navbar/navbar'
import './App.css';
import axios from 'axios';
import Vote from './components/vote/vote';
import Rankings from "./components/rankings/rankings";
import Calculator from "./components/calculator/calculator";
import {
  BrowserRouter,
  Switch,
  Route,
  Link
} from "react-router-dom";



axios.defaults.xsrfCookieName = 'csrftoken'
axios.defaults.xsrfHeaderName = 'X-CSRFToken'

const theme = createMuiTheme({
  palette: {
    primary: {
       main: '#1b2d3a',
    },
    secondary: {
      main: '#69BCFF',
      },
    },
    typography: { 
        useNextVariants: true
    }
})

class App extends Component {
  render() {
    return (
      <MuiThemeProvider theme={theme}>
        <BrowserRouter>
          <Navbar />
          <Switch>
            <Route exact path="/" component={Vote} />
            <Route exact path="/rankings" component={Rankings} />
            <Route exact path="/calculator" component={Calculator} />
          </Switch>
        </BrowserRouter>

      </MuiThemeProvider>
    );
  }
}

export default App;