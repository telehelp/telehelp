import React from "react";
import { Switch, Route } from "react-router-dom";

import Home from "../pages/Home";
import About from "../pages/About";
import Press from "../pages/Press";

const Main = () => {
  return (
    <div>
      <Switch>
        <Route exact path="/" component={Home}></Route>
        <Route exact path="/om-oss" component={About}></Route>
        <Route exact path="/i-media" component={Press}></Route>
      </Switch>
    </div>
  );
};

export default Main;
