from ..AIServices import OpenAIServices
from ..VectorStoreServices import PineConeService
from Utils import DataHelpers, PromptTemplate
import json

class RAG():
    def __init__(self):
        self._openaiservice = OpenAIServices()
        self._pineconeservice = PineConeService()
        self._prompttemplate = PromptTemplate()
        self._datahelper = DataHelpers()

    async def search(self, convo_id: str, app_id: str, question: str):
        vectors_user_request = await self._openaiservice.EmbeddingsOpenAI(text = question)
        similar_vectors = self._pineconeservice.get_vectors(target_vectors = vectors_user_request, app_id = app_id)
        vectors_dict = self._datahelper.createvectorsdict(similar_vectors) 
        multicontext_prompt_dict = self._prompttemplate.create_a_prompt_template(vectors = vectors_dict,
                                                                                            user_request = question, 
                                                                                            promptType='multicontextresponse')
        response = await self._openaiservice.ChatCompletion(user_prompt=multicontext_prompt_dict["user_prompt"], 
                                                         system_prompt=multicontext_prompt_dict["system_prompt"])  
        AIresponse = json.loads(response)
        if not isinstance(AIresponse, list):
            AIresponse = [AIresponse] 
        AIresult_array = []
        for item in AIresponse:
            response_text = item['response']                       
            if item['source'].lower() == 'conversation-history':
                result_object = {            
                "response": response_text,
                "referenceFileName": "History",
                "referenceFilePath": ""
                }
                AIresult_array.append(result_object)
            else:
                entity = vectors_dict[item['source']]                                
                result_object = {            
                "response": response_text,
                "referenceFileName": entity.filename,
                "referenceFilePath": entity.filepath
                }
                AIresult_array.append(result_object) 
        return json.dumps(AIresult_array, indent = 2) 





