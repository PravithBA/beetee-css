import time
from models.lexer_token import LexerToken
from helpers.lexer_token_types import SYM

source = ""
old_source = ""

def main():
    start_time = time.time()
    f = open('dest/main.btcss')
    source = f"{f.read()} "
    variables = {}
    KEYWORDS = [
        SYM.LEFT_BRACE,
        SYM.RIGHT_BRACE,
        SYM.NEW_LINE,
        SYM.TAB,
        SYM.COLON, 
        SYM.SEMI_COLON,
        SYM.SPACE,
        SYM.RIGHT_ROUND,
        SYM.LEFT_ROUND,
        SYM.COMMA,
        SYM.EQUAL,
        SYM.RANGE_START_STOP
    ]
    lexer = LexerToken(source,KEYWORDS)
    lexemes = lexer.get_lexemes()
    lexemes.append("")
    tree = lexer.generate_tree()
    end_time = time.time()
    print(lexemes)
    print(tree)
    print(f"Time took to run: {end_time - start_time}")
    
if __name__ == "__main__":
    main()