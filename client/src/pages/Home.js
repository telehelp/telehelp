import React from "react";

import BackgroundInfo from "../components/BackgroundInfo";
import MainForm from "../components/MainForm";
import FAQ from "../components/FAQ";
import MapView from "../components/MapView";
import MissionStatement from "../components/MissionStatement";
import ThanksTo from "../components/ThanksTo";

function Home() {
  return (
    <div>
      <header className="tele-header">
        <div className="container">
          <h1 className="tele-title">Vardagshjälp i tider av covid-19</h1>
          <h2 className="tele-number">
            <a href="tel:+46766861551">
              <i className="fas fa-mobile icon-before"></i>
              076-686 15 51
            </a>
          </h2>
        </div>
      </header>
      <section id="intro">
        <div className="container">
          <div className="row">
            <div className="col-lg-8">
              <BackgroundInfo />
            </div>
            <div className="col-lg-4">
              <MainForm />
            </div>
          </div>
        </div>
      </section>
      <section className="bg-primary" id="map">
        <div className="container">
          <div className="row">
            <div className="col-md-12">
              <MapView />
            </div>
          </div>
        </div>
      </section>
      <section id="faq">
        <div className="container">
          <div className="row">
            <div className="col-md-12">
              <FAQ />
            </div>
          </div>
        </div>
      </section>
      <section className="bg-primary" id="mission">
        <div className="container">
          <div className="row">
            <div className="col-md-12">
              <h2>Om Telehelp</h2>
              <MissionStatement />
            </div>
          </div>
        </div>
      </section>
      <section id="partners">
        <div className="container">
          <div className="row">
            <div className="col-md-12">
              <ThanksTo />
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}

export default Home;
