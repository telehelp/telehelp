import React from "react";
import FAQ from "../components/FAQ";
import MapView from "../components/MapView";
import ThanksTo from "../components/ThanksTo";
import MainForm from "../components/MainForm";
import BackgroundInfo from "../components/BackgroundInfo";
import NumberPresentation from "../components/NumberPresentation";

function Home() {
  return (
    <div>
      <div className="row">
        <div className="col-md-8">
          <BackgroundInfo />
        </div>
        <div className="col-md-4">
          <NumberPresentation />
          <MainForm />
        </div>
      </div>
      <div className="row">
        <div className="col-md-12">
          <FAQ />
        </div>
      </div>
      <div className="row">
        <div className="col-md-12">
          <MapView />
        </div>
      </div>
      <div className="row">
        <div className="col-md-12">
          <ThanksTo />
        </div>
      </div>
    </div>
  );
}

export default Home;
