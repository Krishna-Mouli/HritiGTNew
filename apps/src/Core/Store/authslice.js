import { createSlice } from "@reduxjs/toolkit";

const initialState = {
    token: null,
    isAuthticated: false,
    user: null
}

const authSlice = createSlice({
    name: 'auth',
    initialState,
    reducers:{
        loginSuccess: (state, action) => {
            state.token = action.payload.token;
            state.isAuthticated = true;
            state.user = action.payload.user
        },
        logout: (state) => {
            state.token = null;
            state.isAuthticated = false;
            state.user = null;
        }
    },
});

export const { loginSuccess, logout } = authSlice.actions; 
export default authSlice.reducer; 