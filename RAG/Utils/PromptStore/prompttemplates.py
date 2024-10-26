import logging 
import os
import json
from typing import List, Dict
import textwrap
from Data import Vectors

from Utils import StringHelpers

class PromptTemplate:
    def __init__(self):
        self.maxcompletiontokenlimit = 15001   
        self.stringhelper = StringHelpers()     

    def create_a_prompt_template(self,
                                 vectors: Dict[str, Vectors] = None,
                                 user_request: str = None, 
                                 promptType: str = None, 
                                 previosly_summarized_content: str = None) -> dict[str,str]:
        try:
            prompt_dict = {}
            if previosly_summarized_content is None:
                previosly_summarized_content = "There is no history for this conversation yet, this is the beginning of the conversation."
            
            if promptType == 'multicontextresponse':
                context = ""
                maxRequestTokens = int(self.maxcompletiontokenlimit) * 0.8
                for key,value in vectors.items():
                    if(self.stringhelper.num_tokens_from_string(f"{context} {value.chunk_content}") > maxRequestTokens):
                        break
                    context += f"\n<source>\n<source-id> \t {key} \t </source-id> \n <source-content> \t {value.chunk_content} \t </source-content> \n </source>"
                context += f"\n<source>\n <source-id> \t conversation-history \t </source-id> \n <source-content> \t {previosly_summarized_content} \t </source-content> \n </source>"

                system_prompt = f"""You are a Human Resources Policy Bot used by the employees of Sonata Software. You provide answer to any question as truthfully as possible in complete sentences based on Sonata's HR policy. \
                            You are provided with excerpts from various policy documents and a summarized transcript of the on going conversation \
                            between you and the user as context. You only use factual information provided in this context or summarized transcript to answer the question. \
                            Use the conversation summary to understand and analyze the on going conversation, sometimes the user might just want to build on the \
                            on going conversation, for such questions use the summary to answer.\r\n The context may contain many sections. Each section contains the source id \
                            and the source content.\r\nBelow is an example of the context with two sections and \
                            conversation summary.  \r\n
                            <context_start>\n
                            <source>\n
                            <source-id> \t Source id 1 \t </source-id>\n
                            <source-content> \t Content 1 \t </source-content>\n
                            </source>\n
                            <source>\n
                            <source-id> \t Source id 2 \t </source-id>\n
                            <source-content> \t Content 2 \t </source-content>\n
                            </source>\n
                            <source>\n
                            <source-id> \t conversation-history \t </source-id>\n
                            <source-content> \t summarized history of the conversation \t </source-content>\n
                            </source>\n
                            <context_end>\n                            
                            You MUST provide the response in the following JSON format,\r\n
                            [{{"source": "<source-id>", "response":"<answer found in the section>"}}, {{"source": "<source-id", "response":"<answer found in section>"}}]\r\n\r\n
                            You include answer identified from each section separately in the response. You will keep each answer brief and to the point. \
                            You NEVER MERGE the sections. You will go through each section one by one and try to find the answer, If you cannot find the answer in a section \
                            for that section you will say "Answer not found" in the response like so, [{{"source": "<source-id>", "response":"Answer not found"}}].\r\n\r\n
                            You MUST identify the gender context of the question. If the question is related to male employees and the context only has information for \
                            female employees, then, don't answer the question.\n"""


                user_prompt = f"""<context_start>{context}\n<context_end> \n                                                                         
                                    Do not provide any information other than what is available in above context.\n
                                    The context has dates in the following format, dd-nov-23 which means dd is the day of the month november in the year 2023 \
                                    in the context the years are mentioned by the last 2 digits, for example, 22 is 2022, 19 is 2019, 23 is 2023, 56 is 2056 etc \
                                    make sure that you take care of these dates while generating your response, make sure that the year in the context is same as the \
                                    year in the user request before generating your response\n                 
                                    user request: {user_request}"""                  

            elif promptType == 'summarization':      
                #here vectors is a List of Dictionaries, use source and reponse to format.    
                answers = []
                for i, item in enumerate(vectors, start=1):  # Start counting from 1
                    answers.append(f"Answer: {i} is {item['response']}\n")
                final_answers = ''.join(answers)                
                system_prompt = """
                    You are an expert in English and summarizing ongoing conversations, you are capable of properly analyzing and converting many conversational \
                    turns into a single consolidated paragraph, you will be given the summarized content for the ongoing conversation which could be empty if the \
                    conversation just started. As you are summarizing a conversation, you need to summarize in third person. \
                    For example, if the conversation just started you can start the summary with "User asked this and the answer given was this" you have \
                    to analyze and build up on this. Remember you are summarizing a conversation not an article or essay. \

                    You will use this summarized conversation content and embed the new conversation turns into this already summarized conversation. \
                    Make sure to capture the essence and key points of the ongoing conversation. The length of the summary should be appropriate for \
                    the length and complexity of the original text, providing a clear and accurate overview without omitting any important information. \

                    The format for the content would be like so: \n
                    <ongoing-summarized-content> \n summary \n </ongoing-summarized-content>\n
                    <New-conversation-turns> \n
                    <Question> \t Question \t </Question>\n
                    <Answer> \t Answer \t </Answer>
                    </New-conversation-turns>

                    Make sure to keep the current essence of the summary going and carefully include the context of the new conversational turns into the summary. \
                    Also make sure to provide your answer in a JSON using the format \
                    "{ "Summary" : "summary" }" 
                    """
                user_prompt = f""""<ongoing-summarized-content> \n{previosly_summarized_content}\n </ongoing-summarized-content>\n
                                    <New-conversation-turns>\n
                                    <Question> \t {user_request} \t </Question>\n
                                    <Answer> \t {final_answers} \t </Answer>\n 
                                    </New-conversation-turns>"""                       

            elif promptType == 'changerequest':
                system_prompt = f"""
                        You are an expert in English grammar and vocabulary. 
                        You will be given a question that was asked by a human along with a summarized version of an ongoing conversation between this Human and 
                        an AI, your job is to better articulate this question asked by the human using the summary so that the AI can understand and respond to 
                        this question effectively. Make the question as clear as possible, you can be descriptive but not too much. Carefully analyze the summary 
                        before you respond. You will be provided with the summary and question as follows. You will provide the newly articulated question from 
                        the perspective of the Human. 

                        <human-question> \t Question \t </human-question>\n
                        <summarized-conversation> \n Summary of Conversation \n </summarized-conversation>\n
                        
                        Make sure you return only the newly articulated question and nothing else.
                        """

                user_prompt = f"""
                        <human-question> \t {user_request} \t </human-question>
                        <summarized-conversation> \n {previosly_summarized_content} \n </summarized-conversation>
                        """   
                                     
            prompt_dict['user_prompt'] = textwrap.dedent(user_prompt).strip()
            prompt_dict['system_prompt'] = textwrap.dedent(system_prompt).strip()

            return prompt_dict
    
        except Exception as e:
            logging.error(f"an error occured \n {str(e)}")

    