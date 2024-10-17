#! ServiceNow Functions
import os
import requests
from requests.auth import HTTPBasicAuth
from ..GoogleCloudServices import GCPTableStorageServiceClient
from Data.Models import ServiceNowTicketDetails
import uuid
import json
from Utils.Helpers import HTMLTableGenerator

class ServiceNow():
    def __init__(self):
        self.instance = os.environ.get('service_now_instance')
        self.username = os.environ.get('service_now_username')
        self.password = os.environ.get('service_now_password')
        self.helper = HTMLTableGenerator()

    def post_service_now_ticket(self, short_description, description, category, priority):
        
        url = f'{self.instance}/api/now/table/incident'
        
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        
        data = {
                "short_description": short_description,
                "description": description,
                "category": category,
                "priority": priority
            }
        
        response = requests.post(url, 
                                 auth=HTTPBasicAuth(self.username, self.password), 
                                 headers=headers, 
                                 json=data)
        
        if response.status_code == 201:
            data = response.json().get('result',[])
            ticket_number = data.get('number')
            self.add_service_now_ticket_details(ticket_number, description, category)
            return (f"Ticket created successfully with the following details: \n ID: {ticket_number} \n Description: {description} \n For further details, please visit your ServiceNow account at abccompany.service-now.com")                 
        else:
            return ('Failed to create ticket')             

    def add_service_now_ticket_details(self, id, subject, category):
        datastore_service = GCPTableStorageServiceClient(model = ServiceNowTicketDetails)
        data = ServiceNowTicketDetails(
            entity_id=str(uuid.uuid4()),
            ticket_id = id,
            ticket_category = category,
            ticket_description = subject
        )
        datastore_service.upsert_data(data = data)   

    def get_service_now_ticket_details(self, ticketid):        
        url = f'{self.instance}/api/now/table/incident?sysparm_query=number={ticketid}'
        headers = {
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        try:            
            response = requests.get(url, auth=HTTPBasicAuth(self.username, self.password), headers=headers)
            response.raise_for_status()             
            ticket_details = response.json().get('result', [])
            if ticket_details:                
                ticket_info = ticket_details[0] 
                important_info = {
                    "Number": ticket_info.get('number'),
                    "Short Description": ticket_info.get('short_description'),
                    "Priority": ticket_info.get('priority'),
                    "State": ticket_info.get('state'),
                    "Created": ticket_info.get('sys_created_on'),
                    "Updated": ticket_info.get('sys_updated_on'),
                    "sys_updated_by": ticket_info.get('sys_updated_by'),
                    "sys_created_by":ticket_info.get('sys_created_by'),
                    "opened_at":ticket_info.get('opened_at'),                    
                }
                return json.dumps(important_info)
            else:
                return 'No ticket found with the specified number.'
        except requests.exceptions.RequestException as e:
            print('An error occurred:', e)

    def get_service_now_ticket_ids(self):
        datastore_service = GCPTableStorageServiceClient(model = ServiceNowTicketDetails)        
        data = datastore_service.get_all_data()    
        html_str = self.helper.convert_to_html(data)       
        return html_str