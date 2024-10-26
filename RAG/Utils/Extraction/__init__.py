from .AzureDocumentIntelligence import Extractor
from .LlamaParse import LlamaParseExtractor

from fastapi import UploadFile

from Data import Extractors
def get_extractor(extractor_logic: Extractors, file_bytes: bytes) -> str:
    extractors = {
        Extractors.AZURE_FORM_RECOGNIZER: Extractor(),
        # Extractors.LLAMA_PARSE: LlamaParseExtractor()
    }
    extractor = extractors[extractor_logic]
    return extractor.extract(file_bytes)
