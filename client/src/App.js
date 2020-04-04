import React from 'react';
import './App.scss';
import RegistrationForm from './components/RegistrationForm';
import FAQ from './components/FAQ';
import TeleHelpBar from './components/TeleHelpBar';
import TeleHelpIntroduction from './components/TeleHelpIntroduction'

class App extends React.Component {
  constructor(props) {
    super(props)
    this.state = {
      time: 0,
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
    const { time } = this.state;

    return (
    <div className="App">
      <div className="container">
        <div className="row">
          <div className="col-12">
            <TeleHelpBar/>
          </div>
        </div>
        <div className="row">
          <div className="col-12">
            <TeleHelpIntroduction/>
          </div>
        </div>
        <div className="row">
          <div className="col-8">
            <div className="introduction">
              <h2> Registrera dig som hjälpare redan idag!</h2>
              <p>The current time is {time}.</p>
              <div className="row">
                <div className="col-6">
                  <img className="photo" src="/young-person.png" alt="Young person bringing bag to a door"></img>
                </div>
                <div className="col-6">
                  <img className="photo" src="/old-people.png" alt="Two happy old people on a bench"></img>
                </div>
              </div>
              <p>
              Genom att skriva upp dig som volontär kan personer som ingår i riskgrupper eller som redan är smittade av corona i ditt närområde ringa till dig för att få hjälp med sysslor som plötsligt blivit svåra på grund av coronakrisen, exempelvis att handla mat eller hämta mediciner.
              </p>
            </div>
          </div>
          <div className="col-4">
            <div className="signup" id="register">
              <RegistrationForm/>
            </div>
          </div>
        </div>
        <div className="row">
          <div className="col-12">
            <FAQ/>
          </div>
        </div>
      </div>
    </div>
  )
  }
}

export default App;
