import React from 'react';
import './App.scss';
import FAQ from './components/FAQ';
import TeleHelpBar from './components/TeleHelpBar';
import MapView from './components/MapView';
import ThanksTo from './components/ThanksTo'
import Footer from './components/Footer';
import MainForm from './components/MainForm';
import BackgroundInfo from './components/BackgroundInfo';


function App() {
    return (
    <div className="App">
      <div className="container">
        <div className="row">
          <div className="col-md-12">
            <TeleHelpBar/>
          </div>
        </div>
        <div className="row">
          <div className="col-md-8">
            <BackgroundInfo/>
          </div>
          <div className="col-md-4">
            <MainForm/>
          </div>
        </div>
        <div className="row">
          <div className="col-md-12">
            <FAQ/>
          </div>
        </div>
        <div className="row">
          <div className="col-md-12">
            <MapView/>
          </div>
        </div>
        <div className="row">
          <div className="col-md-12">
            <ThanksTo/>
          </div>
        </div>
      </div>
      <Footer/>
    </div>
  )
}

export default App;
