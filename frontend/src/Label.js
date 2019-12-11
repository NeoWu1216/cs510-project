import React from 'react';
import { Button, ButtonGroup} from '@material-ui/core';
import { makeStyles } from '@material-ui/core/styles';


const searchStyles = makeStyles(theme => ({
  root: {
    // display: 'flex',
    // flexDirection: 'row',
    // alignItems: "center",
  },

  button: {
    textTransform: 'none',
  }
}))


function LabelGroup(props) {
  const classes = searchStyles();
  const resList = props.data;
  return (<ButtonGroup className={classes.root}>
    {resList.map(x => <Label data={x} key={x.text}/>)}
  </ButtonGroup>)
}




function Label(props) {
  const classes = searchStyles();
  const {data} = props
  const {text, onClick, color} = data

  return (
    <Button onClick={onClick} className={classes.button} color={color}>
      {text}
    </Button>
  )
}

export default LabelGroup;


