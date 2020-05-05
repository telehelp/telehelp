import React from "react";
import "./App.scss";
import TeleHelpBar from "./components/TeleHelpBar";
import Footer from "./components/Footer";
import Main from "./components/Main";

function App() {
  return (
    <div className="App">
      <TeleHelpBar />
      <Main />
      <Footer />
    </div>
  );
}

export default App;
