import React from 'react';
import './App.scss';
import RefreshButton from './components/RefreshButton';
import RegistrationForm from './components/RegistrationForm';

class App extends React.Component {
  constructor(props) {
    super(props)
    this.state = {
      time: 0,
      isRegistering: false
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
    const {time, isRegistering} = this.state;

    return (
    <div className="App">
      <header className="App-header">
        <h1> Sign up for TeleHelp today!</h1>

        <p>The current time is {time}.</p>
        
        <RegistrationForm/>
      </header>
    </div>
  )
  }
}

export default App;
