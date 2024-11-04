import React, { useState } from 'react';
import { Box, Menu, MenuItem, Typography } from '@mui/material';
import { FaUser } from 'react-icons/fa';
import { useSelector } from 'react-redux';

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
      <Box display="flex" alignItems="center" style={{ cursor: 'pointer' }} onClick={handleClick}>
        <FaUser style={{ width: '30px', height: '30px', color: 'white' }} />
        <Typography variant="h6" sx={{ color: 'white', marginLeft: '10px', fontWeight: 'bold', fontFamily: 'monospace, Courier New, Courier' }}>
          Welcome, {user.name}
        </Typography>
      </Box>
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
          <Typography style={{ color: '#000' }}>Logged in {user.email}</Typography>
        </MenuItem>
        {/* <MenuItem onClick={handleClose}>Profile</MenuItem>
        <MenuItem onClick={handleClose}>Settings</MenuItem>
        <MenuItem onClick={handleClose}>Logout</MenuItem> */}
      </Menu>
    </Box>
  );
};