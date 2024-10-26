from enum import Enum

class Chunkers(Enum):
    BASIC_CHUNKER = "basic_chunker"
    RECURSIVE_TOKEN_CHUNKER = "recursive_token_chunker"
    FIXED_TOKEN_CHUNKER = "fixed_token_chunker"
    
