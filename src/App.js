import React, { useState } from 'react';
import Button from '@material-ui/core/Button';
import CircularProgress from '@material-ui/core/CircularProgress';
import { green, red } from '@material-ui/core/colors';
import { makeStyles } from '@material-ui/core/styles';
import axios from 'axios';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';

const apiUrl = 'https://stock-algo.vercel.app';

const useStyles = makeStyles((theme) => ({
  container: {
    display: 'flex',
    flexDirection: 'column',
    minHeight: '100vh',
  },
  header: {
    backgroundColor: 'black',
    color: 'white',
    padding: theme.spacing(2),
    textAlign: 'center',
  },
  footer: {
    backgroundColor: 'black',
    color: 'white',
    padding: theme.spacing(2),
    textAlign: 'center',
    marginTop: 'auto',
  },
  buttonContainer: {
    display: 'flex',
    justifyContent: 'center',
    marginTop: theme.spacing(2),
  },
  button: {
    margin: theme.spacing(1),
  },
  loader: {
    display: 'flex',
    justifyContent: 'center',
    marginTop: theme.spacing(2),
  },
}));

const App = () => {
  const classes = useStyles();
  const [loading, setLoading] = useState(false);

  const handleButtonClick = async (action) => {
    setLoading(true);
    try {
      const response = await axios.get(`${apiUrl}/${action}`);
      toast.success(response.data);
    } catch (error) {
      toast.error('An error occurred while processing your request.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className={classes.container}>
      <header className={classes.header}>
        <h1>InvestIt®</h1>
        <h3 style={{ fontStyle: 'italic', fontWeight: 'lighter' }}>"Where Magic happens while you sip on your PinãColada 🍹"</h3>
      </header>
      <div>
        <div className={classes.buttonContainer}>
          <Button
            variant="contained"
            style={{ backgroundColor: green[500], color: 'white' }}
            className={classes.button}
            onClick={() => handleButtonClick('buy')}
            disabled={loading}
          >
            Run Buy Algo
          </Button>
          <Button
            variant="contained"
            style={{ backgroundColor: red[500], color: 'white' }}
            className={classes.button}
            onClick={() => handleButtonClick('sell')}
            disabled={loading}
          >
            Run Sell Algo
          </Button>
        </div>
        {loading && (
          <div className={classes.loader}>
            <CircularProgress />
          </div>
        )}
      </div>
      <footer className={classes.footer}>
        <p>&copy; 2024 InvestIt®</p>
      </footer>
      <ToastContainer />
    </div>
  );
};

export default App;
