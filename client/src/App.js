import React from "react";
import "./App.scss";
import TeleHelpBar from "./components/TeleHelpBar";
import TeleHelpHeader from "./components/TeleHelpHeader";
import Footer from "./components/Footer";
import Main from "./components/Main";

function App() {
  return (
    <div className="App">
      <TeleHelpBar />
      <TeleHelpHeader />
      <div className="container">
        <Main />
      </div>
      <Footer />
    </div>
  );
}

export default App;
