import React, { useState, useEffect } from 'react';
import logo from './logo.svg';
import './App.css';

function App() {

  function refreshPage() {
    window.location.reload(false);
  }
  
  const [currentTime, setCurrentTime] = useState(0);

  useEffect(() => {
    fetch('/time').then(res => res.json()).then(data => {
      setCurrentTime(data.time);
    });
  }, []);

  return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>The time is {currentTime}.</p>
        <div>
        <button onClick={refreshPage}>What's the current time now then?</button>
        </div>
      </header>
    </div>
  );
}

export default App;
