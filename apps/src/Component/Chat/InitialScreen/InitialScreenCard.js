import { Box, Typography } from "@mui/material";
import { FcConferenceCall } from "react-icons/fc";
import { MdOutlineSupportAgent } from "react-icons/md";
import { IoInformationCircleSharp } from "react-icons/io5";
import { GiNinjaHead } from "react-icons/gi";
import { FaPeopleGroup } from "react-icons/fa6";
import { GiStarShuriken } from "react-icons/gi";

const data = [
    {
        img: <FaPeopleGroup fontSize={30}/>,
        message: "Ask any questions related to your enterprise HR and IT"
    },
    {
        img: <MdOutlineSupportAgent fontSize={30}/>,
        message: "Book conference roomes for your meetings"
    },
    {
        img: <IoInformationCircleSharp fontSize={30}/>,
        message: "Raise help tickets to receive support from agents in ServiceNow"
    },
    {
        img: <GiStarShuriken fontSize={30}/>,
        message: "Report any Bugs using your Organization's Jira portal"
    },
]

export const InitialScreenCard = ({index})=>{

    return(
        <Box className="initialScreenCard" style={{width:'150px', height:'150px', border:'1px solid black', borderRadius:'10px', padding:'10px'}}>
            <Box>
                {data[index].img}
            </Box>
            <Box>
                <Typography style={{fontFamily:'monospace'}}>
                    {data[index].message}
                </Typography>
            </Box>
        </Box>
    )
}