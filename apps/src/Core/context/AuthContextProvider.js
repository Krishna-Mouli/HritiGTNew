// AuthContext.js
import { jwtDecode } from 'jwt-decode';
import React, { createContext, useContext, useState, useEffect } from 'react';
import { useDispatch } from 'react-redux';
import { addUser } from '../Store/UserContext';
import { useNavigate } from 'react-router-dom';
const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
    // const [authToken, setAuthToken] = useState(null);
    const [isAuthenticated, setIsAuthenticated] = useState(false);
    const dispatch = useDispatch()
    // const navigate = useNavigate()
        const currentUrl = window.location.href;
        const token = localStorage.getItem('token');

    useEffect(() => {
        if (token) {
            fetchData(token);
            // window.location.href = `${currentUrl}/layout`;
            setIsAuthenticated(true)
        }
        else {
            // window.location.href = `${currentUrl}/login`;
            setIsAuthenticated(false)

        }
    }, []);

    const storeUserInfo =(userInfo)=>{
        dispatch(
                addUser({
                user: {
                    name: userInfo.name,
                    email: userInfo.email,
                    picture: userInfo.picture,
                },
            })
        );
    }

    const fetchData = (token) => {
        const userInfo = jwtDecode(token)
        storeUserInfo(userInfo)
    };

    return (
        <AuthContext.Provider value={{ fetchData, isAuthenticated }}>
            {children}
        </AuthContext.Provider>
    );
};

export const useAuth = () => useContext(AuthContext);
