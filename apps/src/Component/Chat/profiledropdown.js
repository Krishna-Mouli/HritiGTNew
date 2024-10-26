import React, { useState } from 'react';
import { Box, IconButton, Menu, MenuItem, Typography } from '@mui/material';
import AccountCircleIcon from '@mui/icons-material/AccountCircle';
import jane from '../../Assets/Images/Jane.png';
import {  useSelector } from 'react-redux';

export const ProfileDropdown = () => {
  const [anchorEl, setAnchorEl] = useState(null);
  const open = Boolean(anchorEl);
  const user = useSelector((state) => state.userContext.user);
  const handleClick = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleClose = () => {
    setAnchorEl(null);
  };

  return (
    <Box>        
      <Box display="flex" alignItems="center" style={{cursor:'pointer'}}>               
        <IconButton
          onClick={handleClick}
          size="large"
          edge="start"
          color="inherit"
          aria-label="profile"
          aria-controls={open ? 'profile-menu' : undefined}
          aria-haspopup="true"
          aria-expanded={open ? 'true' : undefined}
        >
        <img 
          src={user?.picture}
          alt="Profile"
          style={{
            width: '55px',
            height: '55px', 
            borderRadius: '50%'
          }}
        />
        </IconButton>
        <Typography variant="h6" sx={{color:'white', marginRight: '10px', fontWeight: 'bold', fontFamily:'monospace, Courier New, Courier' }}>
          Welcome,{user.name}
        </Typography> 
        <Menu
          id="profile-menu"
          anchorEl={anchorEl}
          open={open}
          onClose={handleClose}
          MenuListProps={{
            'aria-labelledby': 'profile-button',
          }}
        >
          <MenuItem disabled>
            <Typography style={{ color: '#000' }}>Logged in using jane.doe@abc-company.com</Typography>
          </MenuItem>
          <MenuItem onClick={handleClose}>Profile</MenuItem>
          <MenuItem onClick={handleClose}>Settings</MenuItem>
          <MenuItem onClick={handleClose}>Logout</MenuItem>
        </Menu>
      </Box>           
    </Box>
  );
};

