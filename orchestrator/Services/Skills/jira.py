#! JIRA Functions
import os
import requests
from requests.auth import HTTPBasicAuth
import json
from ..GoogleCloudServices import GCPTableStorageServiceClient
from Utils.Helpers import HTMLTableGenerator
from Data.Models import JiraTicketDetails
import uuid

class JIRA():
    def __init__(self):
        self.uri = os.environ.get('jira_api_url')
        self.api_token = os.environ.get('jira_auth_key')
        self.username = os.environ.get('jira_username')
        self.helper = HTMLTableGenerator()

    def post_jira_ticket(self, summary, description, issue_type):        
        api_endpoint = f'{self.uri}/rest/api/2/issue'
        
        headers = {
            "Accept": "application/json",
            "Content-Type": "application/json"
        }
        
        data = {
                "fields": {
                    "project": {
                        "key": "KAN" 
                    },
                    "summary": summary,
                    "description": description,
                    "issuetype": {
                        "name": issue_type
                    },                    
                }
            }
        
        response = requests.post(
                    api_endpoint,
                    json=data,
                    headers=headers,
                    auth=HTTPBasicAuth(self.username, self.api_token)
                )
        
        if response.status_code == 201:
            data = response.json()
            self.add_jira_ticket_details(data.get('key'), description, issue_type)
            return f"Issue created successfully with Jira ID: {data.get('id')} \n With key: {data.get('key')} \n With description: {description} \n For further details, please visit your Jira account in abcompany.atlassian.net"
        else:
            return f"Failed to create issue: {response.status_code}, {response.text}"

    def add_jira_ticket_details(self, id, subject, issue_type):
        datastore_service = GCPTableStorageServiceClient(model = JiraTicketDetails)
        data = JiraTicketDetails(
            entity_id=str(uuid.uuid4()),
            jira_ticket_id = id,
            ticket_description = subject,
            ticket_issue_type = issue_type
        )
        datastore_service.upsert_data(data = data)      

    def get_jira_ticket_details(self, ticketid):        
        api_endpoint = f'{self.uri}/rest/api/2/issue/{ticketid}'
        headers = {
            'Content-Type': 'application/json',
        }        
        response = requests.get(
            api_endpoint,
            headers=headers,
            auth=HTTPBasicAuth(self.username, self.api_token)
        )        
        if response.status_code == 200:
            issue_data = response.json()
            issue_info = {
                'Key': issue_data.get('key'),
                'Summary': issue_data['fields'].get('summary'),
                'Description': issue_data['fields'].get('description'),
                'Status': issue_data['fields']['status']['name'] if issue_data['fields'].get('status') else None,
                'Priority': issue_data['fields']['priority']['name'] if issue_data['fields'].get('priority') else None,
                'Assignee': issue_data['fields']['assignee']['displayName'] if issue_data['fields'].get('assignee') else 'Unassigned',
                'Reporter': issue_data['fields']['reporter']['displayName'] if issue_data['fields'].get('reporter') else None,
                'Created': issue_data['fields'].get('created'),
                'Updated': issue_data['fields'].get('updated')
            }
            return json.dumps(issue_info)
        else:
            return (f"Failed to fetch issue: {response.status_code}, {response.text}")

    def get_jira_ticket_ids(self):
        datastore_service = GCPTableStorageServiceClient(model = JiraTicketDetails)        
        data = datastore_service.get_all_data()    
        html_str = self.helper.convert_to_html(data)       
        return html_str