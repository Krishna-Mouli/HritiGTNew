from .jira import JIRA
from .servicenow import ServiceNow
from .conferencerooms import ConferenceRooms

class SkillCatalogue():
    def __init__(self):
        self.class_instances = [JIRA(), ServiceNow(), ConferenceRooms()]            
        self._bind_methods()

    def _bind_methods(self):
       """
       Binds all methods from the classes to the SkillCatalogue instance at runtime.       
       """
       for class_instance in self.class_instances:           
           for method_name in dir(class_instance):
               method = getattr(class_instance, method_name)               
               if callable(method) and not method_name.startswith("__"):                   
                   setattr(self, method_name, method)