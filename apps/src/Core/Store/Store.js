import { configureStore } from '@reduxjs/toolkit';
import appsReducer from './AppSlice'
import authReducer from './authslice';

export default configureStore({
  reducer: {
    apps: appsReducer,
    auth: authReducer,
  },
});