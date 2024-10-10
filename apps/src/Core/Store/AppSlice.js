import { createSlice } from '@reduxjs/toolkit';
 
 
const initialState = {
    messages : [],
    snackBarOpen : false
}
 
export const appsSlice = createSlice({
  name: 'apps',
  initialState,
  reducers: {
    setMessages: (state, action)=>{
        state.messages = action.payload
    },
    setSnackBarOpen : (state, action)=>{
      state.snackBarOpen = action.payload
  },
  }
})
 
export const {
    setMessages, setSnackBarOpen
} = appsSlice.actions
 
export default appsSlice.reducer