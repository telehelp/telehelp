import React from 'react';
import FAQ from './FAQ';
import MapView from './MapView';
import ThanksTo from './ThanksTo'
import MainForm from './MainForm';
import BackgroundInfo from './BackgroundInfo';


function Home() {
    return (
        <div>
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
  )
}

export default Home;