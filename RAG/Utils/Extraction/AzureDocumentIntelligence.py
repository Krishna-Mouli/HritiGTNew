from azure.ai.formrecognizer import DocumentAnalysisClient
from azure.core.credentials import AzureKeyCredential
from typing import List, Optional

class Extractor:
    def __init__(self):
        self.endpoint = 'https://mavin-doc-scanner.cognitiveservices.azure.com/'
        self.api_key = 'f6307f8b1a4f4bca90c8e4a9ead7e8b9'
        self.credential = AzureKeyCredential(self.api_key)
        self.document_analysis_client = DocumentAnalysisClient(endpoint=self.endpoint, credential=self.credential)

    def extract(self, file):
        res = self.azure_document_intelligence_call(file)
        string_content = self.content_formatter_for_azure_form_recognizer(res)
        return string_content

    def azure_document_intelligence_call(self, file):
        try:            
            raw_extracted_content = self.document_analysis_client.begin_analyze_document("prebuilt-document", file)
            result = raw_extracted_content.result()
            return result
        except Exception as e:
            return (f"{e}")

    def content_formatter_for_azure_form_recognizer(self, content) -> str:
        final_string = []
        manager = TableDataManager()
        analyze_result = content

        if analyze_result.tables:
            for table in analyze_result.tables:
                start_index = 0
                end_index = 0
                string_builder = []
                n = len(table.cells) - 1
                max_rows = max(cell.row_index for cell in table.cells) + 1
                max_columns = max(cell.column_index for cell in table.cells) + 1

                table_array = [[None for _ in range(max_columns)] for _ in range(max_rows)]
                for cell in table.cells:
                    table_array[cell.row_index][cell.column_index] = cell.content

                string_builder.append("| " + " | ".join(table_array[0][col] or "----------" for col in range(max_columns)) + " |")
                string_builder.append("|" + "|---------" * max_columns + "|")

                for row in range(1, max_rows):
                    string_builder.append("| " + " | ".join(table_array[row][col] or "----------" for col in range(max_columns)) + " |")

                str1 = "\n".join(string_builder)

                start_index = next((cell.spans[0].offset for cell in table.cells if cell.spans), 0)
                end_index = next((cell.spans[0].offset for cell in reversed(table.cells) if cell.spans), 0)

                print(str1 + "\n")
                manager.add_table_data(start_index, end_index, str1)
        flag = 0
        for para in analyze_result.paragraphs:
            end_index = manager.get_end_index_for_start_index(para.spans[0].offset)
            if end_index is not None:
                content = manager.get_content_for_start_index(para.spans[0].offset)
                str_content = f"\n#TblStrt#\n{content}\n#TblEnd#\n"
                final_string.append(str_content)
                flag = end_index
            else:
                if flag < para.spans[0].offset:
                    str_content = para.content
                    if para.role and para.role.lower() == "sectionheading":
                        str_content = f"\n\n{str_content}\n"
                    final_string.append(str_content)
                elif flag == 0 and para.spans[0].offset == 0:
                    str_content = para.content
                    final_string.append(str_content)

        text = "".join(final_string)
        return text

    
class TableDataManager:
    def __init__(self):
        self.start_indices: List[int] = []
        self.end_indices: List[int] = []
        self.contents: List[str] = []

    def add_table_data(self, start_index: int, end_index: int, content: str):
        self.start_indices.append(start_index)
        self.end_indices.append(end_index)
        self.contents.append(content)

    def get_end_index_for_start_index(self, start_index: int) -> Optional[int]:
        try:
            index = self.start_indices.index(start_index)
            return self.end_indices[index]
        except ValueError:
            return None

    def get_content_for_start_index(self, start_index: int) -> Optional[str]:
        try:
            index = self.start_indices.index(start_index)
            return self.contents[index]
        except ValueError:
            return None

    