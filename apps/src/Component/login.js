import React, { useState, useEffect } from 'react';
import { Box, ThemeProvider, createTheme, Typography, Button } from '@mui/material';
import { useGoogleLogin } from '@react-oauth/google';
import axios from 'axios';
import Google from '../Assets/Images/google.svg';

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
  const [user, setUser] = useState(null);
  const [profile, setProfile] = useState(null);

  const handleLoginSuccess = (credentialResponse) => {
    const token = credentialResponse.credential;

    // Decode the JWT token to get user info
    const userInfo = jwtDecode(token);

    // Dispatch the loginSuccess action to store token and user info in Redux
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
  };

  const handleLoginFailure = (error) => {
    console.error('Login Failed:', error);
  };

  const login = useGoogleLogin({
    onSuccess: (codeResponse) => setUser(codeResponse),
    onError: (error) => console.error('Login Failed:', error)
  });

  useEffect(() => {
    if (user?.access_token) {
      axios.get('https://www.googleapis.com/oauth2/v1/userinfo', {
        headers: {
          Authorization: `Bearer ${user.access_token}`,
          Accept: 'application/json'
        }
      })
      .then((res) => setProfile(res.data))
      .catch((err) => console.error(err));
    }
  }, [user]);

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
        </Box>
        {profile && (
          <Typography variant="body1" sx={{ marginTop: 2 }}>
            Welcome, {profile.name}!
          </Typography>
        )}
      </Box>
    </ThemeProvider>
  );
};