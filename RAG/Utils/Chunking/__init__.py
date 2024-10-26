from .BasicChunking import Chunking
from .RecursiveTokenChunker import RecursiveTokenChunker
from .FixedTokenChunker import FixedTokenChunker

from Data import Chunkers
from typing import List

def get_chunks(chunking_logic: Chunkers, content: str) -> List[str]:
    chunkers = {
        Chunkers.BASIC_CHUNKER: Chunking(),
        Chunkers.RECURSIVE_TOKEN_CHUNKER: RecursiveTokenChunker(),
        Chunkers.FIXED_TOKEN_CHUNKER: FixedTokenChunker(),
    }
    chunking = chunkers[chunking_logic]
    return chunking.split_text(content)


