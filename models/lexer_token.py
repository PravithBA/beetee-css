from helpers.lexer_token_types import LexerType

class LexerToken:
    def __init__(self,lexer_token_type:str,content:str,line:int,start_char_pos:int,end_char_pos:int) -> None:
        self.lexer_token_type = lexer_token_type
        self.content = content
        self.line = line
        self.start_char_pos = start_char_pos
        self.end_char_pos = end_char_pos
    
    def get_lexer_token_type(string:str):
        if len(string) == 1:
            if LexerType.OPEN_CURLY_BRACKETS == string:
                return LexerType.OPEN_CURLY_BRACKETS
            if LexerType.CLOSE_CURLY_BRACKETS == string:
                return LexerType.CLOSE_CURLY_BRACKETS
            if LexerType.SEMI_COLON == string:
                return LexerType.SEMI_COLON
            if LexerType.COLON == string:
                return LexerType.COLON
        if string.startswith("$(") and string.endswith(")"):
            return LexerType.CSS_VARIABLE
        if string.startswith("$"):
            return LexerType.RANGE_IDENTIFIER
        if string.startswith("|") and string.endswith("|"):
            return LexerType.RANGE
        if string.startswith("."):
            return LexerType.ELEMENT_CLASS
        if string.startswith("#"):
            return LexerType.ELEMENT_CLASS
        return string
    
    @classmethod
    def generate_lexer_token(cls, string: str, line: int, start_char_pos: int, end_char_pos: int):
        lexer_token_type = LexerToken.get_lexer_token_type(string)
        return cls(
            lexer_token_type = lexer_token_type,
            content = string,
            line = line,
            start_char_pos = start_char_pos,
            end_char_pos = end_char_pos
        )