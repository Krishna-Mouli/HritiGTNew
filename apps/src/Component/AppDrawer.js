import { Accordion, AccordionDetails, AccordionSummary, Box, IconButton, List, ListItem, ListItemButton, ListItemIcon, ListItemText,  Menu, MenuItem, styled, TextField, Tooltip, Typography } from '@mui/material';

import MuiDrawer from '@mui/material/Drawer';
import { useState } from 'react';
import MenuIcon from '@mui/icons-material/Menu';
import AddCircleIcon from '@mui/icons-material/AddCircle';
import CssBaseline from '@mui/material/CssBaseline';
import { MdChatBubble } from "react-icons/md";
import { IoMenu } from "react-icons/io5";
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import { MdDriveFileRenameOutline } from "react-icons/md";
import { VscDebugRestart } from "react-icons/vsc";
import { ImCross } from "react-icons/im";
import { TiTick } from "react-icons/ti";
import { useDispatch, useSelector } from 'react-redux';
import { setMessages, setSnackBarOpen } from '../Core/Store/AppSlice';
import useApiClient from '../Core/Auth/UseApiClient';




const drawerWidth = 240;

const openedMixin = (theme) => ({
  width: drawerWidth,
  transition: theme.transitions.create('width', {
    easing: theme.transitions.easing.sharp,
    duration: theme.transitions.duration.enteringScreen,
  }),
  overflowX: 'hidden',
});

const closedMixin = (theme) => ({
  transition: theme.transitions.create('width', {
    easing: theme.transitions.easing.sharp,
    duration: theme.transitions.duration.leavingScreen,
  }),
  overflowX: 'hidden',
  width: `calc(${theme.spacing(7)} + 1px)`,
  [theme.breakpoints.up('sm')]: {
    width: `calc(${theme.spacing(8)} + 1px)`,
  },
});

const Drawer = styled(MuiDrawer, {
    shouldForwardProp: (prop) => prop !== 'open',
  })(({ theme, open }) => ({
    width: drawerWidth,
    flexShrink: 0,
    whiteSpace: 'nowrap',
    boxSizing: 'border-box',
    ...(open && {
      ...openedMixin(theme),
      '& .MuiDrawer-paper': openedMixin(theme),
    }),
    ...(!open && {
      ...closedMixin(theme),
      '& .MuiDrawer-paper': closedMixin(theme),
    }),
  }));

  const DrawerHeader = styled('div')(({ theme }) => ({
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'flex-end',
    padding: theme.spacing(0, 1),
    // necessary for content to be below app bar
    ...theme.mixins.toolbar,
  }));

  const CustomTextField = styled(TextField)(({ theme }) => ({
    '& .MuiOutlinedInput-root': {
      borderRadius:'10px',
      '& fieldset': {
        borderColor: 'gray', // Default outline color
      },
      '&:hover fieldset': {
        borderColor: '#3d3d3d', // Outline color on hover
      },
      '&.Mui-focused fieldset': {
        borderColor: '#3d3d3d', // Outline color when focused
      },
    },
    '& .MuiInputBase-input': {
      height: '25px',
      backgroundColor: '#e8e6e3',
      padding: '0 5px',
      fontSize: '12px',
      borderRadius: '10px'
    },
  }));

export const AppDrawer = ()=>{
  const [open, setOpen] = useState(false);
  const [expanded, setExpanded] = useState(false);
  const [anchorEl, setAnchorEl] = useState(null);
  const [isRenameChat, setIsRenameChat] = useState(false);
  const [renameText, setRenameText] = useState('Current Chat');
  const dispatch = useDispatch();
  const apiClient = useApiClient()

  // const classes = useStyles();

  const menuOpen = Boolean(anchorEl);
  const handleClick = (event) => {
    setAnchorEl(event.currentTarget);
  };
  const handleClose = () => {
    setAnchorEl(null);
  };


  const handleDrawerOpen = () => {
    setOpen(true);
  };

  const handleDrawer = () => {
    setOpen((prev) => !prev);
  };

  // const handleExpansion = () => {
  //   handleDrawerOpen();
  //   setExpanded((prevExpanded) => !prevExpanded);
  // };

  const handleCurrentChat = ()=>{
    handleClick();
  }

  const handleRenameChat = ()=>{
    setIsRenameChat(true);
    handleClose();
  }

  const handleRefreshSession = async()=>{
    dispatch(setMessages([]));
    handleClose();
    await refreshSession();
    dispatch(setSnackBarOpen(true));
  }

  const handleRenameChatCancel = ()=>{
    setIsRenameChat(false);
  }

  const handleRenameChange = (event) => {
    setRenameText(event.target.value)
  }

  const refreshSession = ()=>{
    apiClient.post('/session/refresh');
  }

    return(
        <Drawer
          variant='permanent'
          open={open}
          style={{ backgroundColor: '#191b1c' }}
        >
          <DrawerHeader style={{ width: '100%', backgroundColor: '#191b1c' }}>
            <IconButton onClick={handleDrawer} style={{ width: '100%' }}>
              <Box
                style={{
                  width: '100%',
                  display: 'flex',
                  // justifyContent: `${open ? 'end' : 'space-between'}`,
                  justifyContent: 'space-between',
                  alignItems: 'center',
                }}
              >
                {/* {open && (
                  <div>
                    <img src={BalooLogo} width='auto' height='30px' alt='RCP' />
                  </div>
                )} */}
                <Tooltip title='Menu'>
                  <IoMenu color='#e8e6e3'/>
                </Tooltip>
              </Box>
            </IconButton>
          </DrawerHeader>
          <List>
            <ListItem
              onClick={handleClick}
              key='Current Chat'
              disablePadding
              sx={{ display: 'block', color:'#e8e6e3' }}
            >
              <ListItemButton
                className='newChat-btn'
                sx={{
                  minHeight: 48,
                  justifyContent: open ? 'initial' : 'center',
                  px: 2.5,
                  background: '#191b1c',
                  width: '90%',
                  marginLeft: '6%',
                  borderRadius: '30px',
                }}
                
              >
                {
                  isRenameChat ?
                  <Box style={{display:'flex', borderRadius:'10px' }}>
                    {/* <TextField 
                    placeholder='rename'
                    id="outlined-basic" label="" variant="outlined"
                    className={classes.root}
                    // InputProps={{
                    //   style: {
                    //     height: '25px',
                    //     padding: '0 5px',
                    //     backgroundColor: '#e8e6e3',
                    //     fontSize: '12px',
                        
                    //   }
                    // }}
                    InputProps={{
                      classes: {
                        input: classes.input
                      }
                    }}
                    style={{width:'80%', marginRight:'5px', }}
                    /> */}
                    <CustomTextField
                      id="outlined-basic"
                      label=""
                      variant="outlined"
                      style={{ width: '80%', marginRight: '5px', borderRadius:'10px' }}
                      onChange={ handleRenameChange}
                      onClick={(e)=>{e.stopPropagation();}}
                      value={renameText}
                    />
                    <Box onClick={(e)=>{e.stopPropagation(); handleRenameChatCancel()}} style={{display:'flex', alignItems:'center', marginRight:'5px', cursor:'pointer'}}>
                      <TiTick fontSize={20}/>
                    </Box>
                    <Box onClick={(e)=>{e.stopPropagation(); handleRenameChatCancel()}} style={{display:'flex', alignItems:'center', cursor:'pointer'}}>
                      <ImCross fontSize={12}/>
                    </Box> 
                  </Box>
                  
                  :
                  <>
                  <ListItemIcon
                  sx={{
                    minWidth: 0,
                    mr: open ? 3 : 'auto',
                    justifyContent: 'center',
                  }}
                >
                  <Tooltip title={renameText}>
                    <MdChatBubble color='#e8e6e3'/>
                  </Tooltip>
                </ListItemIcon>
                <ListItemText
                  primary={renameText}
                  sx={{ opacity: open ? 1 : 0 }}
                />
                  </>
                
}
              </ListItemButton>
            </ListItem>
            <Menu
              id="basic-menu"
              anchorEl={anchorEl}
              open={menuOpen}
              onClose={handleClose}
              MenuListProps={{
                'aria-labelledby': 'basic-button',
              }}
            >
              <MenuItem onClick={handleRenameChat}><MdDriveFileRenameOutline style={{ marginRight: '8px' }} /> Rename Chat</MenuItem>
              <MenuItem onClick={handleRefreshSession}><VscDebugRestart style={{ marginRight: '8px' }}/> Refresh Session</MenuItem>
            </Menu>
            </List> 
            
            {/* ************************************************** */}
            {/* <Accordion
            expanded={expanded}
            onChange={handleExpansion}
            style={{
              backgroundColor: '#191b1c',
              // marginTop: `${open || expanded ? '0' : '50vh'}`,
            }}
          >
            <Tooltip title="Current Chat">
              <AccordionSummary
                expandIcon={<MdChatBubble style={{color:'#e8e6e3'}}/>}
                aria-controls='panel1-content'
                id='panel1-header'
                style={{ margin: '0px', paddingRight: '20px' }}
              >
                {open ? (
                  <Box
                    style={{
                      width: '100%',
                      display: 'flex',
                      justifyContent: 'start',
                      paddingLeft: '10px',
                      margin: '0px',
                      color:'#e8e6e3'
                    }}
                  >
                    <Typography>Current Chat</Typography>
                  </Box>
                ) : (
                  ''
                )}
              </AccordionSummary>
            </Tooltip>
            <AccordionDetails style={{height:'54vh', overflowY:'auto', overflowX:'hidden'}}>
                  <List>
                    <ListItem
                      // onClick={showUserDashboard}
                      key='Dashboard'
                      disablePadding
                      sx={{ display: 'block' }}
                    >
                      <ListItemButton
                        sx={{
                          minHeight: 48,
                          justifyContent: open ? 'initial' : 'center',
                          px: 2.5,
                        }}
                      >
                        <Tooltip title='Rename Chat'>
                          <ListItemIcon
                            sx={{
                              minWidth: 0,
                              mr: open ? 3 : 'auto',
                              justifyContent: 'center',
                            }}
                            
                          >
                            <MdDriveFileRenameOutline style={{color:'#e8e6e3'}}/>
                          </ListItemIcon>
                        </Tooltip>
                        <ListItemText
                          color='#e8e6e3'
                          primary='Rename Chat'
                          sx={{ opacity: open ? 1 : 0 }}
                          style={{color:'#e8e6e3'}}
                        />
                      </ListItemButton>
                    </ListItem>
                    <ListItem
                      // onClick={showConfigControls}
                      key='Refresh'
                      disablePadding
                      sx={{ display: 'block' }}
                    >
                      <ListItemButton
                        sx={{
                          minHeight: 48,
                          justifyContent: open ? 'initial' : 'center',
                          px: 2.5,
                        }}
                      >
                        <Tooltip title='Refresh Session'>
                          <ListItemIcon
                            sx={{
                              minWidth: 0,
                              mr: open ? 3 : 'auto',
                              justifyContent: 'center',
                            }}
                          >
                            <VscDebugRestart style={{color:'#e8e6e3'}}/>
                          </ListItemIcon>
                        </Tooltip>
                        <ListItemText
                          primary='Refresh Session'
                          sx={{ opacity: open ? 1 : 0 }}
                          style={{color:'#e8e6e3'}}
                        />
                      </ListItemButton>
                    </ListItem>
                </List>
            </AccordionDetails>
          </Accordion> */}


        </Drawer>

        
    )
}