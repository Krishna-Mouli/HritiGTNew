from dataclasses import dataclass

@dataclass
class Tool:
    tools = [
        {
            "type": "function",
            "function":{
                  "name":"get_response_for_IT_queries",
                  "description":"Use this function to get the answer for only IT related queries, if the user query is not an IT query then this function should not be used. Examples of IT queries include, 'How do I change my SAP password', 'how do I activate my O365 subscription', 'how do i reset z scalar', or any such IT related queries.", 
                  "parameters":{
                        "type":"object",
                        "properties":{
                          "question": {
                              "type":"string",
                              "description":"The question that the user asked related to IT."
                          }
                        },
                    "required":["question"]
                }
            }
        },
        {
            "type": "function",
            "function":{
                  "name":"get_response_for_HR_queries",
                  "description":"Use this function to get the answer for only HR related queries, if the user query is not an HR query then this function should not be used. Examples of HR queries include, 'Hou should I record my attendance', 'what should I do if I need to take and unplanned leave due to personal exigencies', 'what is the maximum duration allowed for a sabbatical period?', or any such HR related queries.", 
                  "parameters":{
                        "type":"object",
                        "properties":{
                          "question": {
                              "type":"string",
                              "description":"The question that the user asked related to HR."
                          }
                        },
                    "required":["question"]
                }
            }
        },        
        {
            "type": "function",
            "function": {
                "name": "get_conference_room_details",
                "description": "Get the information regarding all the conference rooms. When you are using this function you will get the response from the function as a HTML table, you need to respond with a HTML table only do not convert it into a mark down table.",            
            }
        },
        {
            "type": "function",
            "function": {
                "name": "post_conference_room_details",
                "description": "Check if the conference room is available in the given time and date if it is then add the conference room booking details along with the booking time to the database",
                "parameters": {
                    "type": "object",
                    "properties": {
                        "date": {
                            "type": "string",                        
                            "description": "The date mentioned in the user query, e.g 4th of auguest, 04/05 in dd-mm or 12/03 in mm-dd or in other formats, always convert this into a standard format which is YYYY-MM-DD, if year is not provided by the user assume it to be 2024."
                        },
                        "conferenceroomnumber": {
                            "type": "integer",
                            "description": "The conference room number which the user wishes to book make suer the number is present in the available conference rooms."
                        },
                        "starttime": {
                            "type": "string",
                            "format": "time",
                            "description": "The start time e.g., 16:00 hours, 04:00 PM, it could be in other formats as well, always convert this into the 24 hour format and make sure it is between 09:00 and 17:00 hours including 09:00 and 17:00"
                        },
                        "endtime": {
                            "type": "string",
                            "format": "time",
                            "description": "The end time e.g., 16:00 hours, 04:00 PM, it could be in other formats as well, always convert this into the 24 hour format and make sure it is between 09:00 and 17:00 hours including 09:00 and 17:00"
                        },
                        "purpose": {
                              "type":"string",
                              "description":"The reason why the user wants to book a conference room, e.g. 'sprint planning', 'team planning' etc, make sure that the purpose is realted to Enterprice work or not , if it is not then tell the user you cannot book the room."
                        },
                    },
                    "required": ["Date", "ConferenceRoomNumber", "starttime", "endtime"]
                }
            }
        },     
        {
            "type": "function",
            "function": {
                "name":"get_conference_room_booking_details",
                "description":"Get the details of all the conference room bookings for a particular user.",
            }
        },
        {
            "type":"function",
            "function":{
                "name":"get_jira_ticket_ids",
                "description":"call this function if the user requests for the ticket ids which are under his name in JIRA portal, this function only provides the tickets ids not the ticket details.call this function if the user requests for getting the raised project tickets.",
            }
        },                   
        {
            "type":"function",
            "function":{
                  "name":"post_jira_ticket",
                  "description":"call a Post API call to post the jira ticket information with respect to the infomation provided in the user's request. These tickets are mostly related to development either in frontend or backend. Usually fall in the category of 'Bug' or 'Story'.", 
                  "parameters":{
                        "type":"object",
                        "properties":{
                              "summary": {
                                  "type":"string",
                                  "description":"The summary of the ticket, a more condenced form of the description, if the user does not provide this use the description to create a summary e.g. 'This is an issue related to a button not working' etc."
                              },
                              "description":{
                                  "type":"string",
                                  "description":"This is a detailed description of the issue"
                              },                              
                              "issue_type":{
                                  "type":"string",
                                  "description":"The type of the issue which only be either 'Bug' or 'Story' nothing else, you are responsible to decide from either of these two, but once conform with the user before raising the ticket."
                              }
                        },
                        "required":["summary","description","priority","components"]
                }
            }
        },
        {
            "type":"function",
            "function":{
                "name":"get_jira_ticket_details",
                "description":"call this function if the user requests for the ticket details for a particular ticket id from Jira portal, this function only provides the ticket details not the ticket ids.",
                "parameters":{
                        "type":"object",
                        "properties":{
                              "ticketid": {
                                  "type":"string",
                                  "description":"The ticket id for which the details are to be fetched"
                              },                              
                        },
                        "required":["ticketid"]
                }
            }
        },   
        {
            "type":"function",
            "function":{
                "name":"get_service_now_ticket_ids",
                "description":"call this function if the user requests for the ticket ids which are under his name in service now portal, this function only provides the tickets ids not the ticket details. call this function if the user requests for getting the raised Support tickets.",
            }
        },                   
        {
            "type":"function",
            "function":{
                  "name":"post_service_now_ticket",
                  "description":"call a Post API call to post the service now ticket information with respect to the infomation provided in the user's request. These tickets are related to support usually fall in the category of 'Hardware', 'Software', 'Network', 'Security', kind of issues.",
                  "parameters":{
                        "type":"object",
                        "properties":{
                              "short_description": {
                                  "type":"string",
                                  "description":"The summary of the ticket, a more condenced form of the description, if the user does not provide this use the description to create a summary e.g. 'This is an issue related to a button not working' etc."
                              },
                              "description":{
                                  "type":"string",
                                  "description":"This is a detailed description of the issue"
                              },
                              "category":{
                                  "type":"string",
                                  "description":"The category of the ticket, e.g. 'Hardware', 'Software', 'Network', 'Security', 'Service Request',  you are responsible to decide from either of these, but once conform with the user before raising the ticket."
                              },
                              "priority":{
                                  "type":"string",
                                  "description":"The priority of the ticket which is a scaled from 1 to 5, e.g. 1, 2, 3, 4, 5 ask the user to provide this, if not you are free to decide but once conform with the user."
                              }
                        },
                        "required":["short_description","description","category","priority"]
                }
            }
        },
        {
            "type":"function",
            "function":{
                "name":"get_service_now_ticket_details",
                "description":"call this function if the user requests for the ticket details for a particular ticket id from service now portal, this function only provides the ticket details not the ticket ids.",
                "parameters":{
                        "type":"object",
                        "properties":{
                              "ticketid": {
                                  "type":"string",
                                  "description":"The ticket id of service now for which the details are to be fetched"
                              },                              
                        },
                        "required":["ticketid"]
                }
            }
        },              
    ]



    system_prompt: str = "You are an assistant who always follows rules you will make sure that the provided rules are met before generating a response. You assist people at large firm named ABC Company you help employees with various office management tasks like, raising help tickets in JIRA, service now, booking conference rooms and answering their IT or HR related queries, you have been given access to some functions to use. Use them appropriately do not make assumptions about what values to plug into functions. Ask for clarification if a user request is ambiguous. If you feel non of the functions can be used to fullfill the user's requests then suggest them with some tool creation example and say, <I'm sorry but I do not possess this capability as of now, if you want me to learn this please register a new skill in my skill catalogue>. Rules to always follow: Rule# Make sure to always respond in HTML format, for example, use para tags, heading tags and other tags whenever needed if you need to use a line break use <br> instead of \n, if you need to respond using a table always respond with a HTML table never use a markdown etc, make sure you always follow this rule before responding, do not send plain strings, make sure it is in HTML format. You are not allowed to respond in any other format other than HTML. You will be punished if you did not responsd in HTML format. You wll never add any button tags, text areas and anchor tags."