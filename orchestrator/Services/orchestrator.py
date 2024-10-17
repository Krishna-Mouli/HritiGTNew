from .AIServices import openai_service
from .Skills import SkillCatalogue
from Utils.tools import Tool
from openai.types.chat import ChatCompletionMessage
import json

class SearchService:
    def __init__(self):        
        self._tools = Tool()
        self._AIobj = openai_service()
        self._services = SkillCatalogue()

    def search(self, query, messages):
        if not any(message["role"] == "system" for message in messages):
            messages.append({"role": "system", "content": self._tools.system_prompt})
        messages.append({"role": "user", "content": query})
        chat_response = self._AIobj.chat_completion_request(
                messages, tools=self._tools.tools
            )       
        assistant_message = chat_response.choices[0].message 
        messages.append(assistant_message)
        if assistant_message.tool_calls:
            for tool_call in assistant_message.tool_calls:
                    function_name = tool_call.function.name
                    function_args = json.loads(tool_call.function.arguments)

                    if function_name == "get_conference_room_details":
                        function_response = self._services.get_conference_room_details()
                    elif function_name == "get_conference_room_booking_details":
                        function_response = self._services.get_conference_room_booking_details()
                    elif function_name == "post_conference_room_details":
                        function_response = self._services.post_conference_room_details(Date = function_args["date"], 
                                                                                   ConferenceRoomNumber = function_args["conferenceroomnumber"], 
                                                                                   starttime = function_args["starttime"], 
                                                                                   endtime = function_args["endtime"],
                                                                                   purpose = function_args["purpose"])                                        
                    # elif function_name == "get_response_for_IT_queries":
                    #     function_response = self._services.get_response_for_IT_queries(question = function_args["question"])    


                    # elif function_name == "get_response_for_HR_queries":
                    #     function_response = self._services.get_response_for_HR_queries(question = function_args["question"]) 


                    if function_name == "post_jira_ticket":
                        function_response = self._services.post_jira_ticket(summary = function_args["summary"], 
                                                                            description = function_args["description"],        
                                                                            issue_type = function_args["issue_type"])
                    elif function_name == "get_jira_ticket_ids":
                        function_response = self._services.get_jira_ticket_ids()                    
                    elif function_name == "get_jira_ticket_details":
                        function_response = self._services.get_jira_ticket_details(ticketid = function_args["ticketid"])


                    elif function_name == "post_service_now_ticket":
                        function_response = self._services.post_service_now_ticket(short_description = function_args["short_description"], 
                                                                                    description = function_args["description"], 
                                                                                    category = function_args["category"],
                                                                                    priority = function_args["priority"])
                    elif function_name == "get_service_now_ticket_ids":
                        function_response = self._services.get_service_now_ticket_ids()
                    elif function_name == "get_service_now_ticket_details":
                        function_response = self._services.get_service_now_ticket_details(ticketid = function_args["ticketid"])
                                                                                                                                 
                    messages.append({
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": function_name,
                        "content": function_response,
                    })
                    chat_response = self._AIobj.chat_completion_request(
                        messages, tools=self._tools.tools
                        )
                    assistant_message = chat_response.choices[0].message
                    messages.append(assistant_message)                    
        return messages