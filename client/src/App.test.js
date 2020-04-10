import React from "react";
import { render } from "@testing-library/react";
import App from "./App";
import { Provider } from "react-redux";
import configureStore from "redux-mock-store";
import { FormStatus } from "./actions";
import { BrowserRouter } from "react-router-dom";
import MutationObserver from "mutation-observer";

global.MutationObserver = MutationObserver;

test("renders header", () => {
  const initialState = {
    registration: { progress: FormStatus.REGISTER_DETAILS },
  };
  const mockStore = configureStore();

  let store = mockStore(initialState);
  const { getByText } = render(
    <Provider store={store}>
      <BrowserRouter>
        <App />
      </BrowserRouter>
    </Provider>
  );
  const linkElement = getByText(/Hjälp dina grannar att klara vardagen!/i);
  expect(linkElement).toBeInTheDocument();
});

test("test registration regex", () => {
  const initialState = {
    registration: { progress: FormStatus.REGISTER_DETAILS },
  };
  const mockStore = configureStore();

  let store = mockStore(initialState);
  const { getByText } = render(
    <Provider store={store}>
      <BrowserRouter>
        <App />
      </BrowserRouter>
    </Provider>
  );
  const linkElement = getByText(/Hjälp dina grannar att klara vardagen!/i);
  expect(linkElement).toBeInTheDocument();
});
