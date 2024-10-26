import React, { useState, useEffect } from 'react';
import { Box, ThemeProvider, createTheme, Typography, Button } from '@mui/material';
import { useGoogleLogin } from '@react-oauth/google';
import axios from 'axios';
import Google from '../Assets/Images/google.svg';
import { loginSuccess } from '../Core/Store/authslice';
import { useDispatch, useSelector } from 'react-redux';
import { jwtDecode } from 'jwt-decode';
import { GoogleLogin } from '@react-oauth/google';
import { addUser } from '../Core/Store/UserContext';
import { redirect, useNavigate } from 'react-router-dom';
import { useAuth } from '../Core/context/AuthContextProvider';
const theme = createTheme({
  palette: {
    background: {
      dark: '#000000',
    },
    text: {
      primary: '#ffffff'
    }
  },
  typography: {
    fontFamily: 'Courier, monospace',
    fontWeight: 'bold',
    h2: {
      fontWeight: 900,
    },
  },
});

// const TypewriterText = ({ text, speed = 50 }) => {
//   const [displayText, setDisplayText] = useState('');

//   useEffect(() => {
//     let index = 0;
//     const typingInterval = setInterval(() => {
//       if (index < text.length) {
//         setDisplayText((current) => current + text[index]);
//         index++;
//       } else {
//         clearInterval(typingInterval);
//       }
//     }, speed);

//     return () => clearInterval(typingInterval);
//   }, [text, speed]);

//   return <span>{displayText}</span>;
// };

export const LoginPage = () => {
  // const [user, setUser] = useState(null);
const [profile, setProfile] = useState(null);
const user = useSelector((state) => state.userContext.user);
const token = useSelector((state) => state.auth.token);
const isAuthenticated = useSelector((state)=>state.auth.isAutheticated)
const dispatch = useDispatch();
const navigate = useNavigate()
// const { isAuthenticated } = useAuth();
// console.log(user)
  const storeUserInfo =(userInfo)=>{
      dispatch(
      loginSuccess({
        token,
        user: {
          name: userInfo.name,
          email: userInfo.email,
          picture: userInfo.picture,
        },
      })
    );
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

  const handleLoginSuccess = (credentialResponse) => {
    const token = credentialResponse.credential;

    // Decode the JWT token to get user info
    const userInfo = jwtDecode(token);
    console.log(userInfo)
    // Dispatch the loginSuccess action to store token and user info in Redux
   storeUserInfo(userInfo)
   localStorage.setItem('token', token);
   navigate('/layout')
  };

  const handleLoginFailure = (error) => {
    console.error('Login Failed:', error);
  };

  const login = useGoogleLogin({
    onSuccess: (codeResponse) => {handleLoginSuccess(codeResponse)},
    onError: (error) =>{ handleLoginFailure(error)}
  });

  useEffect(() => {
    let token = localStorage.getItem('token')
    // // console.log(access_token)
    // if (access_token) {
    //   axios.get('https://www.googleapis.com/oauth2/v1/userinfo', {
    //     headers: {
    //       Authorization: `Bearer ${access_token}`,
    //       Accept: 'application/json'
    //     }
    //   })
    //   .then((res) => {
    //     // console.log(res.data)
    //     storeUserInfo(res.data);
    //     navigate('/layout');
    //   })
    //   .catch((err) => console.error(err));
    // }
    if(token){
    const userInfo = jwtDecode(token)
    storeUserInfo(userInfo)
    navigate('/layout')
    }
  }, [isAuthenticated]);

  return (
    <ThemeProvider theme={theme}>
      <Box 
        sx={{
          bgcolor: 'background.dark',
          color: 'text.primary',
          minHeight: '100vh',
          display: 'flex',
          flexDirection: 'column',
          justifyContent: 'center',
          alignItems: 'center',
          padding: 2,
          boxSizing: 'border-box',
        }}
      >
        <Typography 
          variant="h2"
          sx={{
            background: 'linear-gradient(to right, darkcyan, cyan)',
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent',
            fontFamily: 'Courier New',
            marginBottom: 4,
          }}
        >
          Hello there, I'm Hriti!
        </Typography>
        <Box
          sx={{
            display: 'flex',
            alignItems: 'center',
            gap: 2,
          }}
        >
        <GoogleLogin
          onSuccess={handleLoginSuccess}
          onError={handleLoginFailure}
        />
        {/* <button onClick={login}>Sign in with Google</button> */}
        </Box>
        {user.name && (
          <Typography variant="body1" sx={{ marginTop: 2 }}>
            Welcome, {user.name}!
          </Typography>
        )}
      </Box>
    </ThemeProvider>
  );
};