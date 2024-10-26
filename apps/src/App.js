import './App.css';
import Store from './Core/Store/Store';
import { Layout } from './Layout/Layout';
import { Provider } from 'react-redux';
import { Component, useEffect, useState } from 'react';
import { LoginPage } from './Component/login'
import { BrowserRouter, Routes, Route,Navigate, useNavigate, redirect } from "react-router-dom";
import { AuthProvider } from './Core/context/AuthContextProvider';
function App() {
  


return (
<Provider store={Store}>

    <BrowserRouter>
      <Routes>
          <Route path="/" element={<Navigate to="/login" replace />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/layout" element={<Layout/>}/>
      </Routes>
    </BrowserRouter>

</Provider>
  );
}

export default App;
