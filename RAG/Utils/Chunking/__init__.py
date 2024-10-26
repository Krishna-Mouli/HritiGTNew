from .BasicChunking import Chunking

from Data import Chunkers
from typing import List

def get_chunks(chunking_logic: Chunkers, content: str) -> List[str]:
    chunkers = {
        Chunkers.BASIC_CHUNKER: Chunking()
    }
    chunking = chunkers[chunking_logic]
    return chunking.chunk(content)


