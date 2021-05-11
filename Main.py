from Tokenizer import Tokenizer
from Parser import Parser
import os


DIR_PATH = "LW_Files"
MAIN_FILE = "MainFile.txt"

GRAMMAR = {
    "NAME": (r"[A-Z]+", None),
    "PARAM": (r"n[1-9]\d*", lambda val: int(val[1:])),
    "VAR": (r"x\d+", None),
    "PLUS": (r"\+", None),
    "MINUS": (r"-", None),
    "NOT_ZERO": (r"!=\s*0", None),
    "CONST": (r"0|1", lambda val: int(val)),
    "ASSIGN": (r":=", None),
    "BEGIN": (r"begin", None),
    "END": (r"end", None),
    "LOOP": (r"loop", None),
    "WHILE": (r"while", None),
    # Whitespace Characters or #-Comments
    "WHITESPACE": (r"\s|#.*\n", None)
}


def init_file():
    if MAIN_FILE not in os.listdir(DIR_PATH):
        with open(f"{DIR_PATH}/{MAIN_FILE}", "w") as file:
            file.write("")

    return f"{DIR_PATH}/{MAIN_FILE}"


def parse_file(parser, file_path) -> str:
    with open(file_path, "r") as file:
        program = file.read()

    parser.parse(program)
    return program


def shell(parser, file_path, program_cache=""):
    program = ""

    while True:
        cmd = input("$> ")
        if cmd.lower() in ["q", "quit", "c", "close"]:
            break
        elif cmd.lower() in ["run", "r"]:
            try:
                parser.parse(program)
                program_cache += program
                program = ""
            except SyntaxError as err:
                print(f"{err}")
        elif cmd.lower() in ["save", "s"]:
            try:
                parser.parse(program)
                program_cache += program
                program = ""
            except SyntaxError as err:
                print(f"Did not save because current code caused Error:\n{err}")
            else:
                with open(file_path, "w") as file:
                    file.write(program_cache)
        else:
            program += cmd + "\n"

if __name__ == '__main__':
    file_path = init_file()

    tokenizer = Tokenizer(GRAMMAR)
    parser = Parser(tokenizer)

    program = parse_file(parser, file_path)
    shell(parser, file_path, program)
