from helpers.lexer_token_types import SYM
from typing import List

class LexerToken():
    def __init__(self,source,KEYWORDS) -> None:
        self.whitespace = SYM.SPACE
        self.lexemes = []
        self.lexeme = ""
        self.string = source
        self.KEYWORDS:List[str] = KEYWORDS
    
    def get_lexemes(self) -> list:
        for index, char in enumerate(self.string):
            if char != self.whitespace and char != SYM.NEW_LINE:
                self.lexeme += char
            if index + 1 < len(self.string):
                next_char = self.string[index+1]
                if (next_char in self.KEYWORDS or next_char == self.whitespace or char in self.KEYWORDS or next_char in SYM.NEW_LINE) and char != self.whitespace:
                    if self.lexeme != "":
                        self.lexemes.append(self.lexeme)
                        self.lexeme = ""
        return self.lexemes
    
    def generate_lex_collection(self) -> dict:
        variables = {}
        tree = {}
        ranges = {}
        
        id_string = ''
        last_id_string = ''
        last_attribute = ''

        current_attribute = ''
        current_value = ''
        current_range_name = ''
        current_range = []

        block_ongoing = False
        attribute_ongoing = False
        value_ongoing = False
        range_obgoing = False

        len_lexemes = len(self.lexemes)
        
        for index,lex in enumerate(self.lexemes):
            if index + 1 < len_lexemes:
                next_lexeme = self.lexemes[index + 1]
                pass
            prev_lexeme = self.lexemes[index - 1]
            if lex == SYM.COMMA:
                continue
            if lex == SYM.RANGE_START_STOP:
                if range_obgoing:
                    ranges[current_range_name] = current_range
                    current_range_name = ""
                    current_range = []
                range_obgoing = not range_obgoing
                continue
            if lex == SYM.LEFT_BRACE:
                block_ongoing = True
                attribute_ongoing = True
                tree[id_string] = {}
                continue
            elif lex == SYM.RIGHT_BRACE:
                block_ongoing = False
                statement_ongoing = False
                attribute_ongoing = False
                value_ongoing = False
                if current_attribute != "":
                    tree[id_string][current_attribute] = current_value[:-1]
                id_string = ""
                current_attribute = ""
                current_value = ""
                continue
            if lex == SYM.COLON:
                value_ongoing = True
                attribute_ongoing = False
                # current_attribute = ""
                continue
            elif lex == SYM.SEMI_COLON:
                value_ongoing = False
                statement_ongoing = False
                attribute_ongoing = True
                if block_ongoing:
                    tree[id_string][current_attribute] = current_value[:-1]
                current_attribute = ""
                current_value = ""
                if not block_ongoing:
                    id_string = ""
                continue
            if range_obgoing and lex != SYM.COMMA:
                current_range.append(lex)
                continue
            if lex == SYM.EQUAL:
                if next_lexeme == SYM.RANGE_START_STOP:
                    current_range_name = prev_lexeme
                else:
                    variables[prev_lexeme] = next_lexeme
                continue
            if not block_ongoing:
                id_string += f"{lex} "
            if attribute_ongoing and block_ongoing:
                current_attribute += f"{lex}"
            if value_ongoing:
                current_value += f"{lex} "
        return {
            "variables":variables,
            "tree":tree,
            "ranges" :ranges
        }

    def get_css_from_tree(tree:dict) -> str:
        css_string = ""
        for i,(block_key,block) in enumerate(tree.items()):
            if block_key.count("$") > 0:
                continue
            css_string += f"{block_key}"+"{\n"
            for i, (attr,value) in enumerate(block.items()):
                    css_string += '\n{}{}: {};'.format(SYM.TAB, attr, value)
            css_string += "\n\n}\n\n"
        return css_string