import {Box, IconButton, Snackbar} from '@mui/material';
import { AppDrawer } from '../Component/AppDrawer';
import CssBaseline from '@mui/material/CssBaseline';
import { Chat } from '../Component/Chat/Chat';
import { ProfileDropdown } from '../Component/Chat/profiledropdown';
import { Fragment, useState, useEffect } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { setSnackBarOpen } from '../Core/Store/AppSlice';
import CloseIcon from '@mui/icons-material/Close';
import { useAuth } from '../Core/context/AuthContextProvider';
import { useNavigate } from 'react-router-dom';
import { jwtDecode } from 'jwt-decode';
import { addUser } from '../Core/Store/UserContext';
import { loginSuccess } from '../Core/Store/authslice';
export const Layout = ()=>{
    const dispatch = useDispatch();
    const {snackBarOpen} = useSelector((state) => state.apps);
    const user = useSelector((state) => state.userContext.user);
    const token = useSelector((state) => state.auth.token);
    const navigate = useNavigate()
    const isAuthenticated = useSelector((state)=>state.auth.isAutheticated)

    // const {isAuthenticated}= useAuth()
    const handleSnackBarClose = (event, reason) => {
        if (reason === 'clickaway') {
          return;
        }
   
        dispatch(setSnackBarOpen(false));
      };
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
      
useEffect(() => {
    const token = localStorage.getItem('token')

    if(!isAuthenticated ){
        if(token){
            const userInfo = jwtDecode(token)
            storeUserInfo(userInfo)
        }
        else {
            navigate('/login')
        }
    }

  }, []);
    const action = (
        <Fragment>
            <IconButton
            size="small"
            aria-label="close"
            color="inherit"
            onClick={handleSnackBarClose}
            >
            <CloseIcon fontSize="small" />
            </IconButton>
        </Fragment>
    );
 
    return(
        <Box style={{display:'flex',}}>
            <AppDrawer/> 
            <Box style={{ position: 'absolute', top: '20px', right: '50px' }}>
                <ProfileDropdown />
            </Box>
            <Chat/>
 
            <Snackbar
                anchorOrigin={{ vertical: 'top', horizontal: 'right' }}
                open={snackBarOpen}
                autoHideDuration={3000}
                onClose={handleSnackBarClose}
                message="Session Refreshed"
                action={action}
            />
        </Box>
    )
}