import React from 'react';
import './App.css';
import { makeStyles } from '@material-ui/core/styles';
import {AppBar, Toolbar, Typography, IconButton} from '@material-ui/core'
import {TextField, MenuItem, FormControl, Select} from '@material-ui/core'

import AccountCircle from '@material-ui/icons/AccountCircle';
import SearchResList from './searchResList.js'
import LabelGroup from './Label.js'

var prefix = "cs510-project.herokuapp.com"
if (process.env.NODE_ENV !== 'production') {
  prefix = "127.0.0.1:8000"
}

const useStyles = makeStyles(theme => ({
  root: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
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
    display: "flex",
    alignItems: "center",
    height: "20vh",
    // alignContent: "center"
  },
  formControl: {
    width: "30vw",
  },
  labelGroup: {
    flex: 1, 
    justifyContent: 'center'
  },
  resList: {
    display: 'flex',
    color : 'red',
    // display: 'flex',
    // height: '60vh',
    // alignItems: 'center',
    // justifyContent: 'center'
  }
}));

function App() {
  let topics = ['All', 'Dataset', 'Graphic', 'Video', 'Similarity', 'Object Detection', 'Convolution', 'Points']


  function buttonObj(text) {
    return {text:text, onClick:onButtonClick, color:(state.topic==text ? 'primary': 'default')}
  }

  const [state, setState] = React.useState({
    searchMode : '',
    searchText : '',
    topic: topics[0],
    topicData: {'All':[]},
    searchResState: [],
  });



  React.useEffect(() => {
    // Update the document title using the browser API
    fetch("http://"+prefix+"/query_all",
            {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                }
            }
    ).then(res => res.json()).then(json => {
      console.log(json)
      return setState(
      {...state, 
        topicData: json,
      }
    )})
  }, []);

  React.useEffect(()=>{
    console.log(state)
    setState({...state, searchResState: state.topicData['All']})
  },[state.topicData])

  
  function onButtonClick(e) {
    let clicked = e.target.innerText
    console.log('Clicked', clicked)
    console.log(state.topicData[clicked], state.allData)
    setState({...state, searchResState: state.topicData[clicked], topic: clicked})
  }


  


  function onMenuItemChange(e) {
    setState({...state, searchMode: e.target.value})
  }

  function onChange(e) {
    setState({...state, searchText: e.target.value})
  }

  function onSearch() {
      if (state.topic === 'All') {
        fetch("http://"+prefix+"/query_title_paragraph",
            {
                method: 'POST',
                body: JSON.stringify({queryString:state.searchText}),
                headers: {
                    'Content-Type': 'application/json'
                }
            }
        ).then(res => res.json()).then(json => setState({...state, searchResState:json}))
      } else {
        fetch("http://"+prefix+"/query_topic",
        {
            method: 'POST',
            body: JSON.stringify({queryString:state.searchText, topicString: state.topic}),
            headers: {
                'Content-Type': 'application/json'
            }
        }
        ).then(
          res => res.json()
        ).then(
          json => setState({...state, searchResState:json})
        )
      }
  }

  const classes = useStyles();

  let buttons = topics.map(buttonObj)


  return (
    <div className={classes.root}>
      <AppBar position="sticky">
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
            onChange={onChange}
        />
      </div>
      <LabelGroup data={buttons} className={classes.labelGroup}/>
      <SearchResList data={state.searchResState} className={classes.resList}/>
      
    </div>
  );
}

export default App;
