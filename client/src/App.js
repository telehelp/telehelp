import React from "react";
import "./App.scss";
import TeleHelpBar from "./components/TeleHelpBar";
import Footer from "./components/Footer";
import Main from "./components/Main";
import { Provider } from "react-redux";

function App() {
  const ReduxProvider = ({ children, reduxStore }) => (
    <Provider store={reduxStore}>{children}</Provider>
  );

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
