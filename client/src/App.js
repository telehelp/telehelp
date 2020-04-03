import React from 'react';
import logo from './logo.svg';
import './scss/App.scss';
import RefreshButton from './components/RefreshButton';

class App extends React.Component {
  constructor(props) {
    super(props)
    this.state = {
      time: 0
    }
  }

  componentDidMount() {
    fetch('/time')
    .then(res => res.json())
    .then(data => this.setState({
        time: data.time
      }
    ))
    .catch(console.log('error setting time'))
  }

  render() {
    const {time} = this.state;

    return (
    <div className="App">
      <header className="App-header">
        <img src={logo} className="App-logo" alt="logo" />
        <p>The time is {time}.</p>
        <RefreshButton >{"Refresh the page"}</RefreshButton>
        <a
          className="App-link"
          href="https://reactjs.org"
          target="_blank"
          rel="noopener noreferrer"
        >
          Learn React
        </a>
      </header>
    </div>
  )
  }
}

export default App;
