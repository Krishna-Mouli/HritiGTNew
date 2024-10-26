import { Box, hexToRgb, Skeleton, Stack, TextareaAutosize, Typography } from "@mui/material"
import { LuSendHorizonal } from 'react-icons/lu';
import { FaMicrophoneSlash } from 'react-icons/fa';
import { MessageContainer } from "./MessageContainer";
import { useEffect, useRef, useState } from "react";
import { InitialScreen } from "./InitialScreen/InitialScreen";
import useApiClient from "../../Core/Auth/UseApiClient";
import { useDispatch, useSelector } from 'react-redux';
import { setMessages } from "../../Core/Store/AppSlice";
import { FaPlus } from "react-icons/fa";
import { AiOutlinePlus } from "react-icons/ai";
import {Button, VisuallyHiddenInput} from "@mui/material";

const dummyData = [
    {
        "content": "You are an assistant at a large firm you help employees with various office management tasks like raising help tickets, book conference rooms and answer their HR related queries, you have been given access to some functions to use. Use them appropriately do not make assumptions about what values to plug into functions. Ask for clarification if a user request is ambiguous. If you need to respond using a table always respond with a HTML table never use a markdown.",
        "role": "system"
    },
    {
        "content": "give me the details of available conference rooms",
        "role": "user"
    },
    {
        "content": null,
        "role": "assistant"
    },
    {
        "content": "<table border=\"1\" class=\"dataframe\">\n  <thead>\n    <tr style=\"text-align: right;\">\n      <th>Conference Room Number</th>\n      <th>Occupancy Limit</th>\n      <th>Reserved For</th>\n      <th>Projector</th>\n      <th>Location</th>\n    </tr>\n  </thead>\n  <tbody>\n    <tr>\n      <td>1</td>\n      <td>6</td>\n      <td>Employees</td>\n      <td>yes</td>\n      <td>Floor 2 section 1</td>\n    </tr>\n    <tr>\n      <td>2</td>\n      <td>10</td>\n      <td>Clients</td>\n      <td>yes</td>\n      <td>Floor 2 section 3</td>\n    </tr>\n    <tr>\n      <td>3</td>\n      <td>10</td>\n      <td>Clients</td>\n      <td>yes</td>\n      <td>Floor 3 section 2</td>\n    </tr>\n    <tr>\n      <td>4</td>\n      <td>6</td>\n      <td>Employees</td>\n      <td>no</td>\n      <td>Floor 3 section 3</td>\n    </tr>\n    <tr>\n      <td>5</td>\n      <td>8</td>\n      <td>Employees</td>\n      <td>no</td>\n      <td>Floor 4 section 1</td>\n    </tr>\n    <tr>\n      <td>6</td>\n      <td>8</td>\n      <td>Employees</td>\n      <td>yes</td>\n      <td>Floor 4 section 2</td>\n    </tr>\n    <tr>\n      <td>7</td>\n      <td>10</td>\n      <td>Clients</td>\n      <td>yes</td>\n      <td>Floor 4 section 3</td>\n    </tr>\n    <tr>\n      <td>8</td>\n      <td>8</td>\n      <td>Employees</td>\n      <td>no</td>\n      <td>Floor 5 section 1</td>\n    </tr>\n    <tr>\n      <td>9</td>\n      <td>8</td>\n      <td>Employees</td>\n      <td>no</td>\n      <td>Floor 5 section 2</td>\n    </tr>\n    <tr>\n      <td>10</td>\n      <td>6</td>\n      <td>Employees</td>\n      <td>yes</td>\n      <td>Floor 5 section 3</td>\n    </tr>\n  </tbody>\n</table>",
        "role": "tool"
    },
    {
        "content": "Here are the details of the available conference rooms:\n\n<table border=\"1\" class=\"dataframe\">\n  <thead>\n    <tr style=\"text-align: right;\">\n      <th>Conference Room Number</th>\n      <th>Occupancy Limit</th>\n      <th>Reserved For</th>\n      <th>Projector</th>\n      <th>Location</th>\n    </tr>\n  </thead>\n  <tbody>\n    <tr>\n      <td>1</td>\n      <td>6</td>\n      <td>Employees</td>\n      <td>yes</td>\n      <td>Floor 2 section 1</td>\n    </tr>\n    <tr>\n      <td>2</td>\n      <td>10</td>\n      <td>Clients</td>\n      <td>yes</td>\n      <td>Floor 2 section 3</td>\n    </tr>\n    <tr>\n      <td>3</td>\n      <td>10</td>\n      <td>Clients</td>\n      <td>yes</td>\n      <td>Floor 3 section 2</td>\n    </tr>\n    <tr>\n      <td>4</td>\n      <td>6</td>\n      <td>Employees</td>\n      <td>no</td>\n      <td>Floor 3 section 3</td>\n    </tr>\n    <tr>\n      <td>5</td>\n      <td>8</td>\n      <td>Employees</td>\n      <td>no</td>\n      <td>Floor 4 section 1</td>\n    </tr>\n    <tr>\n      <td>6</td>\n      <td>8</td>\n      <td>Employees</td>\n      <td>yes</td>\n      <td>Floor 4 section 2</td>\n    </tr>\n    <tr>\n      <td>7</td>\n      <td>10</td>\n      <td>Clients</td>\n      <td>yes</td>\n      <td>Floor 4 section 3</td>\n    </tr>\n    <tr>\n      <td>8</td>\n      <td>8</td>\n      <td>Employees</td>\n      <td>no</td>\n      <td>Floor 5 section 1</td>\n    </tr>\n    <tr>\n      <td>9</td>\n      <td>8</td>\n      <td>Employees</td>\n      <td>no</td>\n      <td>Floor 5 section 2</td>\n    </tr>\n    <tr>\n      <td>10</td>\n      <td>6</td>\n      <td>Employees</td>\n      <td>yes</td>\n      <td>Floor 5 section 3</td>\n    </tr>\n  </tbody>\n</table>",
        "role": "assistant"
    }
]

export const Chat = ()=>{
    const [messageTextarea, setMessageTextarea] = useState('');
    const [messagesArray, setMessagesArray] = useState([]);
    const [showSkeletonLoader, setSkeletonLoader] = useState(false);
    const userQuestionRef = useRef(null);
    const apiClient = useApiClient();
    const dispatch = useDispatch();
    const {messages} = useSelector((state) => state.apps);

    useEffect(()=>{
        console.log('messages useeffect', messages)
        userQuestionRef.current?.scrollIntoView({ behavior: 'smooth' });
    },[messages])

    const handleSendClick = async () => {
        let userMessage = {
            role: 'user',
            content: messageTextarea
        };
        // let newMessagesArray = [...messagesArray, userMessage];
        let newMessagesArray = [...messages, userMessage];
        // setMessagesArray(newMessagesArray);
        dispatch(setMessages(newMessagesArray))

        setSkeletonLoader(true);
        const apiResponse = await chatCall();
        console.log('apiresp', apiResponse)
        const botResponse = apiResponse[apiResponse.length - 1];
        console.log('botResponse', botResponse)
        // setMessagesArray(prevMessages => [...prevMessages, botResponse]);
        dispatch(setMessages([...newMessagesArray, botResponse]));
        console.log('API call completed', apiResponse);
        setMessageTextarea('');
        setSkeletonLoader(false);
    };
    
    const simulateApiCall = () => {
        return new Promise((resolve) => {
            setTimeout(() => {
                resolve(dummyData);
            }, 2000); 
        });
    };

    const chatCall = async()=>{
        const payload = {
            "message": messageTextarea,
            "converseid":"112"
        }
        const response = await apiClient.post('/api/search/chat', payload);
        return response.data
    }
    const handleDocUpload = () =>{

    }

    const uploadDoc = async()=>{
        const payload = {}
        
    }


    return(
        <Box style={{display:'flex', flexDirection:'column', height:'100vh', width:'100%' , color:'white' , backgroundColor:'black'}}>
            <Box style={{height:'85%', paddingInline:'20%', paddingTop:'50px', overflow:'auto' ,color:'white' , backgroundColor:'black'}}>
                {
                    messages.length <= 0 
                    ?
                    <Box style={{height:'100%'}}>
                        <InitialScreen />
                    </Box>
                    :
                    messages.map((item, index)=>{
                        const isBot = item.role === "user" ? false : true;
                        const itemProps = item.role === 'user' ?  {ref : userQuestionRef} : {} ;
                        return <Box {...itemProps}><MessageContainer  isBot={isBot} message={item.content}/></Box>
                    })
                }
                {
                    showSkeletonLoader &&
                    <Stack spacing={0} style={{height:'400px'}}>
                        <Skeleton variant="text" sx={{ fontSize: '1.5rem', color:'red', backgroundColor:'linear-gradient(90deg, rgb(9 9 121 / 19%) 35%, rgba(239, 240, 240, 1) 100%)' }} />
                        <Skeleton variant="text" animation="wave" sx={{ fontSize: '1.5rem' }} />
                        <Skeleton variant="text" animation="wave" sx={{ fontSize: '1.5rem' }} />
                        <Skeleton variant="text" animation="wave" sx={{ fontSize: '1.5rem', width:'80%' }} />
                      </Stack>
                }
            </Box>
            <Box style={{height:'15%', paddingInline:'20%'}}>
                <Box display="flex" justifyContent="center">
                    <Typography variant="h5" sx={{ fontWeight: 'bold', fontFamily:'monospace, Courier New, Courier' }}>
                        ABC Company
                    </Typography> 
                </Box> 
                <Box className="userInputTextarea" style={{ width: '100%', backgroundColor: '#191b1c', borderRadius:'20px', paddingInline:'10px', display:'flex', flexDirection:'row', alignItems:'center' , padding:'10px'}}>
                <Box>
                    <Button
                        component="label"
                        role={undefined}
                        variant="text"
                        tabIndex={-1}
                        startIcon={<FaPlus />}
                        >
                        <input
                            type="file"
                            onChange={(event) => console.log(event.target.files)}
                            style={{display:'none'}}
                            multiple
                        />
                    </Button>
                </Box>
                <TextareaAutosize
                value={messageTextarea}
                onChange={(event)=>setMessageTextarea(event.target.value)}
                placeholder='Send Message'
                className='completeQuestion-textarea'
                style={{
                    resize: 'none',
                    width: '100%',
                    border: 'none',
                    minHeight: '16px',
                    maxHeight: '50px',
                    backgroundColor: '#191b1c',
                    outline: 'none',
                    paddingLeft: '10px',
                    borderRadius: '10px ',
                    color:'#e8e6e3'
                }}
                ></TextareaAutosize>
                <Box>
                    <LuSendHorizonal size = '1.5em' color='#e8e6e3  ' style={{cursor:'pointer'}} onClick={handleSendClick}/>
                </Box>
                </Box>
                <Box style={{display:'flex', justifyContent:'center', marginTop:'10px'}}>
                    <Typography style={{fontSize:'10px', color:'#e8e6e3'}}>
                        AI may provide incorrect info, please verify important details. Your privacy matters.
                    </Typography>
                </Box>
            </Box>

        </Box>
    )
}