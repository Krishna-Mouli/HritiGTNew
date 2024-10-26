import './App.css';
import Store from './Core/Store/Store';
import { Layout } from './Layout/Layout';
import { Provider } from 'react-redux';
import { Component, useEffect, useState } from 'react';
import { LoginPage } from './Component/login'

function App() {

  return (
    <Provider store={Store}>
      <div>        
        <Layout />
      </div>
    </Provider>
  );
}

export default App;
