import React from 'react';
import Typography from '@material-ui/core/Typography';
import Paper from '@material-ui/core/Paper'
import Link from '@material-ui/core/Link';
import { makeStyles } from '@material-ui/core/styles';
import ThumbUpAltIcon from '@material-ui/icons/ThumbUpAlt';
import IconButton from '@material-ui/core/IconButton';


const searchStyles = makeStyles(theme => ({
  root: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: "center",
    
  },
  searchRes: {
    padding: theme.spacing(3, 2),
    width: '65vw',
    marginBottom: "5vh",
  },
}))


function SearchResList(props) {
  const classes = searchStyles();
  const resList = props.data;
  return (<div className={classes.root}>
    {resList.map(x => <SearchRes data={x} onLike={props.onLike}/>)}
  </div>)
}




function SearchRes(props) {
  const classes = searchStyles();


  const {data} = props
  const {title, link, paragraph} = data;

  return (
    <Paper className={classes.searchRes}>
      <Typography variant="h6" component="h3">
        <Link href={link}>
          {title}
        </Link>
      </Typography>
      <Typography component="p" variant="caption">
        {link}
      </Typography>
      <Typography component="p">
        {paragraph}
      </Typography>
      <IconButton aria-label="like" onClick={()=>props.onLike(title)}>
            <ThumbUpAltIcon/>
      </IconButton>

    </Paper>
  )
}

export default SearchResList;


