//let registrationState = 0
export const setRegistrationProgress = (nextProgress) => ({
  type: "SET_REGISTRATION_PROGRESS",
  state: nextProgress,
});

export const setPhoneNumber = (phoneNumber) => ({
  type: "SET_NUMBER",
  number: phoneNumber,
});

export const FormStatus = {
  REGISTER_DETAILS: "REGISTER_DETAILS",
  BAD_DETAILS: "BAD_DETAILS",
  VERIFY_NUMBER: "VERIFY_NUMBER",
  VERIFICATION_FAILED: "VERIFICATION_FAILED",
  REGISTRATION_COMPLETE: "REGISTRATION_COMPLETE",
};

// export const setVisibilityFilter = filter => ({
//   type: 'SET_VISIBILITY_FILTER',
//   filter
// })

// export const toggleTodo = id => ({
//   type: 'TOGGLE_TODO',
//   id
// })

// export const VisibilityFilters = {
//   SHOW_ALL: 'SHOW_ALL',
//   SHOW_COMPLETED: 'SHOW_COMPLETED',
//   SHOW_ACTIVE: 'SHOW_ACTIVE'
// }
