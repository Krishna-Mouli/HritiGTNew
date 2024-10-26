import { createSlice } from '@reduxjs/toolkit';
 
const initialState = {
    user: {},
};
const userContext = createSlice({
    name: 'userContext',
    initialState,
    reducers: {
        addUser: (state, action) => {
            state.user = action.payload.user;
        }
    }})
    export const {
        addUser
    } = userContext.actions;

export default userContext.reducer;