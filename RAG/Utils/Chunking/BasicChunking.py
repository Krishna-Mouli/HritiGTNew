from typing import List
import logging
import tiktoken
import math

class Chunking:
    def __init__(self):
        self._compl_context_max_tokens = 500

    def split_text(self, content: str) -> List[str]:
        """ This function splits the content into segments uses conventional logic"""
        content_segments = []
        tokens = self.num_tokens_from_string(content,None) #you can add your encoding type in place of None if need or by default it uses the cl100k_base encoding
        overlap_token_count = 100 
        tolerance_count = 10   

        logging.info(f"Executing SplitContentV2. Content length: {len(content)}, Total Tokens: {tokens}")

        if tokens > self._compl_context_max_tokens:
            list_table = content.split("#TblStrt#")
            list_temp = []
            for item in list_table:
                end_index = item.find("#TblEnd#")
                if end_index > 0:
                    temp_arr = item.split("#TblEnd#")
                    list_temp.append(f"#TblStrt#!@^{temp_arr[0]}!@^#TblEnd#")
                    list_temp.append(temp_arr[1])
                else:
                    list_temp.append(item)
            list_str = []
            for item in list_temp:
                if item.startswith("#TblStrt#"):
                    list_str.extend(item.split("!@^"))
                else:
                    list_str.extend(item.splitlines() + item.split('. '))
            max_segments = math.ceil(tokens / self._compl_context_max_tokens)
            segment_max_token_count = tokens/int(max_segments)
            str_accumulator = ""
            overlap_str = ""
            table_content = False
            for i in range(len(list_str)):
                trimmed_str = list_str[i].strip()
                if trimmed_str == "#TblStrt#":
                    table_content = True
                    str_accumulator += "\n"
                elif trimmed_str == "#TblEnd#":
                    table_content = False
                else:
                    str_accumulator += f"{trimmed_str}" 
                    str_accumulator += "\n" if table_content else ". "
                    str_token_count = self.num_tokens_from_string(str_accumulator, None)

                    if str_token_count > segment_max_token_count and not table_content:
                        overlap_str += f"{trimmed_str}. "

                    if len(overlap_str) > 0 and table_content:
                        overlap_str = ""

                    if str_token_count > segment_max_token_count + overlap_token_count and not table_content:
                        content_segments.append(str_accumulator)
                        str_accumulator = overlap_str
                        overlap_str = ""
                        logging.info(f"Split Segment created. Segment Length: {len(str_accumulator)}, Token Count: {str_token_count}")

            content_segments.append(str_accumulator)
        else:
            content = content.replace("#TblStrt#", "").replace("#TblEnd#", "")
            content_segments.append(content)

        logging.info(f"SplitContentV2 completed. Content split into {len(content_segments)} segments")
        return content_segments        

    def num_tokens_from_string(self, content: str, encoding_name: str = None) -> int:
        """Returns the number of tokens in a given text string."""
        if encoding_name is None:
            encoding_name = 'cl100k_base'
        encoding = tiktoken.get_encoding(encoding_name)
        num_tokens = len(encoding.encode(content))
        return num_tokens