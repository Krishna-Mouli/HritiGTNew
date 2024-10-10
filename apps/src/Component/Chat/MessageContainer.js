import { Box, TextareaAutosize, Typography } from "@mui/material";
import { FaUserAstronaut } from "react-icons/fa";
import { GiFishMonster } from "react-icons/gi";
import { RiAliensFill } from "react-icons/ri";
import { FaUser } from "react-icons/fa";
import { RiRobot3Fill } from "react-icons/ri";
import jane from '../../Assets/Images/Jane.png';
import LLM from '../../Assets/Images/LLM.png';

export const MessageContainer = ({isBot, message})=>{

    return(
        <Box style={{display:'flex', flexDirection:'column', marginBottom:`${isBot ? "80px" : "20px"}`}}>
            <Box style={{display:'flex', }}> 
                <Box style={{marginRight:'10px'}}>
                    {
                        isBot ? 
                        <img src={LLM} alt="Profile" style={{ width: 30, height: 30, borderRadius: '50%' }} />
                        :
                        <img src={jane} alt="Profile" style={{ width: 40, height: 40, borderRadius: '50%' }} />
                    }   
                    
                </Box>
                <Box>
                    <Typography fontWeight={"bold"} fontSize={'20px'} fontFamily={'monospace, Courier New, Courier'}>
                        { isBot ?
                            "hriti"
                            :
                            "jane doe"
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
                            background:'#111313',
                            color:'#e8e6e3',
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