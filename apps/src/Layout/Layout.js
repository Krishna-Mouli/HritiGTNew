import {Box, IconButton, Snackbar} from '@mui/material';
import { AppDrawer } from '../Component/AppDrawer';
import CssBaseline from '@mui/material/CssBaseline';
import { Chat } from '../Component/Chat/Chat';
import { ProfileDropdown } from '../Component/Chat/profiledropdown';
import { Fragment, useState } from 'react';
import { useDispatch, useSelector } from 'react-redux';
import { setSnackBarOpen } from '../Core/Store/AppSlice';
import CloseIcon from '@mui/icons-material/Close';
 
export const Layout = ()=>{
    const dispatch = useDispatch();
    const {snackBarOpen} = useSelector((state) => state.apps);
   
    const handleSnackBarClose = (event, reason) => {
        if (reason === 'clickaway') {
          return;
        }
   
        dispatch(setSnackBarOpen(false));
      };
 
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