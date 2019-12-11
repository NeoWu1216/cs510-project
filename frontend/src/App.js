import React from 'react';
import './App.css';
import { makeStyles } from '@material-ui/core/styles';
import AppBar from '@material-ui/core/AppBar';
import Toolbar from '@material-ui/core/Toolbar';
import Typography from '@material-ui/core/Typography';
import AccountCircle from '@material-ui/icons/AccountCircle';
import IconButton from "@material-ui/core/IconButton";
import TextField from '@material-ui/core/TextField';
import InputLabel from '@material-ui/core/InputLabel';
import MenuItem from '@material-ui/core/MenuItem';
import FormControl from '@material-ui/core/FormControl';
import Select from '@material-ui/core/Select';
import SearchResList from './searchResList.js'

var prefix = "cs510-project.herokuapp.com"
if (process.env.NODE_ENV !== 'production') {
  prefix = "127.0.0.1:8000"
}

const useStyles = makeStyles(theme => ({
  root: {
    flexGrow: 1,
  },
  menuButton: {
    marginRight: theme.spacing(2),
  },
  title: {
    flexGrow: 1,
  },
  userButtons: {
    marginLeft: "auto",
    marginRight: -12
  },
  searchBar: {
    marginLeft: "5vw",
    marginRight: "5vw",
    display: "flex",
    alignItems: "center",
    height: "40vh",
    alignContent: "center"
  },
  formControl: {
    width: "20vw",
  },
  resList: {
    color : 'red',
    paddingLeft: 200,
    
    // display: 'flex',
    // height: '60vh',
    // alignItems: 'center',
    // justifyContent: 'center'
  }
}));

function App() {
  const resList = [
    {title: 'Hello world', paragraph: 'Lopism Aifoei idie'},
    {title: 'gg', paragraph: 'oigj'} 
  ];

  const [state, setState] = React.useState({
    searchMode : '',
    searchText : '',
  });

  const [searchResState, setSearchResState] = React.useState([]);

  function onMenuItemChange(e) {
    setState({searchMode: e.target.value})
  }

  function onSearch() {
      fetch("http://"+prefix+"/query_title_paragraph",
          {
              method: 'POST',
              body: JSON.stringify({queryString:'cv'}),
              headers: {
                  'Content-Type': 'application/json'
              }
          }
      ).then(res => res.json()).then(json => setSearchResState(json))
  }

  const classes = useStyles();

  return (
    <div className={classes.root}>
      <AppBar position="fixed">
        <Toolbar variant="dense">
          <Typography variant="h6" className={classes.title}>
            Computer Vision Paper Search
          </Typography>
          <span className={classes.userButtons}>
            <IconButton color="inherit" aria-label="Edit">
              <AccountCircle />
            </IconButton>
          </span>
        </Toolbar>
      </AppBar>
      <div className={classes.searchBar}>
        <FormControl variant="outlined" className={classes.formControl}>
          <Select
              labelId="demo-simple-select-outlined-label"
              id="demo-simple-select-outlined"
              value={state.searchMode}
              onChange={onMenuItemChange}
          >
            <MenuItem value="">
              <em>None</em>
            </MenuItem>
            <MenuItem value={10}>Search Papers</MenuItem>
            <MenuItem value={20}>Search Paragraphs</MenuItem>
            <MenuItem value={30}>Recommend Papers</MenuItem>
          </Select>
        </FormControl>
        <TextField
            id="outlined-full-width"
            label="CV papers to search"
            style={{ margin: 5 }}
            placeholder=""
            fullWidth
            margin="normal"
            InputLabelProps={{
              shrink: true,
            }}
            variant="outlined"
            onKeyPress={(ev) => {
                console.log(`Pressed keyCode ${ev.key}`);
                if (ev.key === 'Enter') {
                    // Do code here
                    onSearch();
                    ev.preventDefault();
                }
            }}
        />
      </div>
      <SearchResList data={searchResState} className={classes.resList}/>
    </div>
  );
}

export default App;
