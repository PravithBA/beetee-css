import time
from models.lexer_token import LexerToken
from helpers.lexer_token_types import SYM
from copy import deepcopy
from sys import argv
from watchdog.observers import Observer
from watchdog.events import LoggingEventHandler

print(argv)

source = ""
old_source = ""

btcss_path = argv[1]
css_path = argv[2]

def main():
    start_time = time.time()
    f = open(btcss_path)
    source = f"{f.read()} "
    f.close()
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
    lex_collection:dict = lexer.generate_lex_collection()
    tree:dict = lex_collection["tree"]
    end_time = time.time()
    # print(*lexemes, sep = "\n")
    ranges:dict = lex_collection["ranges"]
    new_tree:dict = deepcopy(tree)
    for index ,(block_key, block) in enumerate(tree.items()):
        block_key:str = block_key
        block:dict = block
        valid_ranges = []
        temp_tree = deepcopy(tree)
        temp_current_tree = {block_key:deepcopy(block)}
        if block_key.count("$") > 0:
            block_keys_to_be_deleted = [block_key]
            for sub_id_index,sub_id in enumerate(block_key.replace(" ","-").split("-")):
                if sub_id.replace("$","") in ranges:
                    valid_ranges.append(sub_id.replace("$",""))
                    range_key = sub_id.replace("$","")
                    range = ranges[range_key]
                    for i, (temp_block_key,temp_block) in enumerate(temp_current_tree.items()):
                        if temp_block_key.count("$") > 0:
                            block_keys_to_be_deleted.append(temp_block_key)
                        temp_current_tree = deepcopy(replace_with_range_items(temp_block,range_key,range,temp_block_key))
                        temp_tree.update(temp_current_tree)
            for block_key_to_be_deleted in block_keys_to_be_deleted:
                if block_key_to_be_deleted in temp_tree:
                    del temp_tree[block_key_to_be_deleted]
            new_tree.update(temp_tree)

    css_string = LexerToken.get_css_from_tree(new_tree)
    f = open(css_path,"w")
    f.write(css_string)
    f.close()
    # print(f"Time took to run: {end_time - start_time}")

def replace_with_range_items(block:dict,range_key:str,range:list,block_key:str):
    new_block = {}
    for range_item in range:
        new_block[block_key.replace(f"${range_key}",range_item)] = deepcopy(block)
        for i , (attr,value) in enumerate(block.items()):
            value:str = value
            if value.count(f"${range_key}") > 0:
                new_value = value.replace(f"${range_key}",range_item)
                new_block[block_key.replace(f"${range_key}",range_item)][attr] = new_value
            pass
    return new_block

if __name__ == "__main__":
    event_handler = LoggingEventHandler()
    observer = Observer()
    observer.schedule(event_handler,btcss_path,True)
    observer.start()
    try:
        while True:
            main()
            time.sleep(1)
    finally:
        observer.stop()
        observer.join()
        