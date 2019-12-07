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
    marginLeft: 200,
    marginRight: 200,
    display: "flex",
    alignItems: "center",
    height: "100vh",
    justifyContent: "center"
  }
}));

function App() {
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
              value=""
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
        />
      </div>
    </div>
  );
}

export default App;
