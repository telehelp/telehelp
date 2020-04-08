
const initialState = {
    progress: 0,
    message: "Registrera dig som volontär!"
};

const registration = (state = initialState, action) => {
    switch (action.type) {
        case 'ADD_DETAILS':
            return Object.assign({}, state, {
                progress: state.progress++
            })
        default:
            return state
    }
}
  
export default registration