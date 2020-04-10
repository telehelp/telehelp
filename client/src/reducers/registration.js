import { FormStatus } from "../actions";

const initialState = {
  progress: FormStatus.REGISTER_DETAILS,
  number: "123123",
};

const registration = (state = initialState, action) => {
  switch (action.type) {
    case "SET_REGISTRATION_PROGRESS":
      // For reasons unknown, this fails with ++
      return Object.assign({}, state, {
        progress: action.state,
      });
    case "SET_NUMBER":
      return Object.assign({}, state, {
        number: action.number,
      });
    default:
      return state;
  }
};

export default registration;
