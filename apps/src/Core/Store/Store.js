import { configureStore } from '@reduxjs/toolkit';

import appsReducer from './AppSlice'

export default configureStore({
  reducer: {
    apps: appsReducer,
  },
});