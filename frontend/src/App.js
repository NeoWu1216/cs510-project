import React from 'react';
import './App.css';
import { makeStyles } from '@material-ui/core/styles';
import {AppBar, Toolbar, Typography, IconButton} from '@material-ui/core'
import {TextField, MenuItem, FormControl, Select} from '@material-ui/core'

import AccountCircle from '@material-ui/icons/AccountCircle';
import SearchResList from './searchResList.js'
import LabelGroup from './Label.js'

import Drawer from '@material-ui/core/Drawer';
import List from '@material-ui/core/List';
import Divider from '@material-ui/core/Divider';
import ListItem from '@material-ui/core/ListItem';
import ListItemIcon from '@material-ui/core/ListItemIcon';
import ListItemText from '@material-ui/core/ListItemText';
import InboxIcon from '@material-ui/icons/MoveToInbox';
import MailIcon from '@material-ui/icons/Mail';

var prefix = "cs510-project.herokuapp.com"
if (process.env.NODE_ENV !== 'production') {
  prefix = "127.0.0.1:8000"
}

const useStyles = makeStyles(theme => ({
  root: {
    display: 'flex',
    marginRight:240,
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
  },
    drawerPaper: {
        width: 240,
    },
}));

function App() {
  let topics = ['All', 'Dataset', 'Graphic', 'Video', 'Similarity', 'Object Detection', 'Convolution', 'Points']


  function buttonObj(text) {
    return {text:text, onClick:onButtonClick, color:(state.topic==text ? 'primary': 'default')}
  }

  const [state, setState] = React.useState({
    searchMode : 'Search Titles',
    searchText : '',
    topic: topics[0],
    topicData: {'All':[]},
    searchResState: [{title:'Loading...'}],
    userLikedPapersTitle: [],
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
      return setState(
      {...state, 
        topicData: json,
      }
    )})
  }, []);

  React.useEffect(()=>{
    setState({...state, searchResState: state.topicData['All'].slice(0, 200)})
  },[state.topicData])

  
  function onButtonClick(e) {
    let clicked = e.target.innerText
    setState({...state, searchResState: state.topicData[clicked], topic: clicked})
  }


  function onLike(title) {
      let newlikedpapers = state.userLikedPapersTitle.concat([title]);
      newlikedpapers = [... new Set(newlikedpapers)];
      setState({...state, userLikedPapersTitle: newlikedpapers});
  }


  function onMenuItemChange(e) {
    if (e.target.value === 'Search Titles') {
      setState({...state, searchMode: e.target.value, topic:'All', searchResState: state.topicData['All'].slice(0, 200)})
    } else {
      setState({...state, searchMode: e.target.value, searchResState: []})
    }
    if (e.target.value === 'Recommend Papers' ) {
        fetch("http://"+prefix+"/query_similar",
            {
                method: 'POST',
                body: JSON.stringify({queryString:state.userLikedPapersTitle}),
                headers: {
                    'Content-Type': 'application/json'
                }
            }
        ).then(res => res.json()).then(json => setState({...state, searchResState:json}))
    }
    // console.log(e.target.value)
    // setState({...state, })
  }

  function onChange(e) {
    setState({...state, searchText: e.target.value})
  }

  async function onSearch() {
      await setState({...state, searchResState:[{paragraph:'Loading...'}]})
      if (state.searchMode === 'Search Paragraphs') {
        await fetch("http://"+prefix+"/query_title_paragraph",
            {
                method: 'POST',
                body: JSON.stringify({queryString:state.searchText}),
                headers: {
                    'Content-Type': 'application/json'
                }
            }
        ).then(res => res.json()).then(json => setState({...state, searchResState:json}))
      } else if (state.searchMode === 'Search Titles') {
        await fetch("http://"+prefix+"/query_topic",
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
            <MenuItem value={'Search Titles'}>Search Titles</MenuItem>
            <MenuItem value={'Search Paragraphs'}>Search Paragraphs</MenuItem>
            <MenuItem value={'Recommend Papers'}>Recommend Papers</MenuItem>
          </Select>
        </FormControl>

        { (state.searchMode === 'Recommend Papers') ? null :
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
        }
      </div>
      <LabelGroup data={buttons} className={classes.labelGroup} hidden={state.searchMode!=='Search Titles'}/>
      <SearchResList data={state.searchResState} className={classes.resList} onLike={onLike}/>



        <Drawer
            className={classes.drawer}
            variant="permanent"
            classes={{
                paper: classes.drawerPaper,
            }}
            anchor="right"
        >
            <div className={classes.toolbar} />
                Welcome User!
                {state.userLikedPapersTitle}
            <Divider />
            <List>
                {['Liked Papers'].map((text, index) => (
                    <ListItem button key={text}>
                        <ListItemIcon>{index % 2 === 0 ? <InboxIcon /> : <MailIcon />}</ListItemIcon>
                        <ListItemText primary={text} />
                    </ListItem>
                ))}
            </List>
        </Drawer>
    </div>
  );
}

export default App;
