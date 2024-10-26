import { configureStore } from '@reduxjs/toolkit';
import appsReducer from './AppSlice'
import authReducer from './authslice';
import userContext from './UserContext';

export default configureStore({
  reducer: {
    apps: appsReducer,
    auth: authReducer,
    userContext:userContext
  },
});