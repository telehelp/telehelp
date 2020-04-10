import React from "react";
import { Switch, Route } from "react-router-dom";

import Home from "../pages/Home";
import About from "../pages/About";
import Press from "../pages/Press";

const Main = () => {
  return (
    <Switch>
      <Route exact path="/" component={Home}></Route>
      <Route exact path="/about" component={About}></Route>
      <Route exact path="/press" component={Press}></Route>
    </Switch>
  );
};

export default Main;
