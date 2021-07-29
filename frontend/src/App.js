import React, { Component } from "react";
import { MuiThemeProvider, unstable_createMuiStrictModeTheme as createMuiTheme } from '@material-ui/core/styles';  
import Nav from './components/tabs/tabs'
import './App.css';
import axios from 'axios';

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
      <MuiThemeProvider theme = { theme }>
        <Nav />
      </MuiThemeProvider>
    );
  }
}

export default App;