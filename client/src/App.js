import React from "react";
import "./App.scss";
import TeleHelpBar from "./components/TeleHelpBar";
import Footer from "./components/Footer";
import Main from "./components/Main";

function App() {
  return (
    <div className="App">
      <div className="container">
        <div className="row">
          <div className="col-md-12">
            <TeleHelpBar />
          </div>
        </div>
        <Main />
      </div>
      <Footer />
    </div>
  );
}

export default App;
