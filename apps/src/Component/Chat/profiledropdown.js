import React, { useState } from 'react';
import { Box, IconButton, Menu, MenuItem, Typography } from '@mui/material';
import AccountCircleIcon from '@mui/icons-material/AccountCircle';
import jane from '../../Assets/Images/Jane.png';

export const ProfileDropdown = () => {
  const [anchorEl, setAnchorEl] = useState(null);
  const open = Boolean(anchorEl);

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
            src={jane}
            alt="Profile"
            style={{ width: 55, height: 55, borderRadius: '50%' }} // Adjust size as needed
          />
        </IconButton>
        <Typography variant="h6" sx={{ marginRight: '10px', fontWeight: 'bold', fontFamily:'monospace, Courier New, Courier' }}>
          Welcome, Jane Doe
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

