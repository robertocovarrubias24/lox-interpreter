import sys
from scanner import Scanner
from parser import Parser
from interpreter import Interpreter


def run(source):
    scanner = Scanner(source)
    tokens = scanner.scan_tokens()

    parser = Parser(tokens)
    statements = parser.parse()

    interpreter = Interpreter()
    interpreter.interpret(statements)


def run_file(path):
    with open(path, "r", encoding="utf-8") as file:
        run(file.read())


def main():
    if len(sys.argv) != 2:
        print("Usage: python lox.py [script]")
        return

    run_file(sys.argv[1])


if __name__ == "__main__":
    main()