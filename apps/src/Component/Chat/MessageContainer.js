import { Box, TextareaAutosize, Typography } from "@mui/material";
import { FaUserAstronaut } from "react-icons/fa";
import { GiFishMonster } from "react-icons/gi";
import { RiAliensFill } from "react-icons/ri";
import { FaUser } from "react-icons/fa";
import { RiRobot3Fill } from "react-icons/ri";
import jane from '../../Assets/Images/Jane.png';
import LLM from '../../Assets/Images/LLM.png';

import { useSelector } from "react-redux";

export const MessageContainer = ({isBot, message})=>{

  const user = useSelector((state) => state.userContext.user);

    return(
        <Box style={{display:'flex', flexDirection:'column', marginBottom:`${isBot ? "80px" : "20px"}`}}>
            <Box style={{display:'flex', }}> 
                <Box style={{marginRight:'10px'}}>
                    {
                        isBot ? 
                        <img src={LLM} alt="Profile" style={{ width: 30, height: 30, borderRadius: '50%' }} />
                        :
                        <FaUser style={{ width: '30px', height: '30px', borderRadius: '50%' }} />
                    }   
                    
                </Box>
                <Box>
                    <Typography fontWeight={"bold"} fontSize={'20px'} fontFamily={'monospace, Courier New, Courier'}>
                        { isBot ?
                            "hriti"
                            :
                            user.name
                        }
                    </Typography>
                </Box>
            </Box>
            <Box style={{paddingLeft:'40px'}}>
                {
                    isBot ?
                    <Box dangerouslySetInnerHTML={{ __html: message }} >
                    </Box>
                    :
                    <TextareaAutosize 
                        readOnly
                        style={{
                            background:'rgb(0 0 0)',
                            color:'white',
                            width:'100%',
                            resize:'none',
                            border:'none',
                            outline: 'none',
                            fontSize:'16px',
                            
                        }}
                    >
                        {message}
                    </TextareaAutosize>
                }
                
            </Box>
        </Box>
    )
}