import sys, os
from pathlib import Path
from tokenizer import Tokenizer
from parser import Parser
from translator import Translator
import webbrowser
"""
MD2HTML is a conversion program from the Markdown format to the HTML format.

This file is the MD2HTML entry file. It takes two arguments in the form of file paths and carries out the conversion. 

Example usage:

    python main.py documents/in.md documents.out.html

The software is provided WITHOUT WARRANTY OF ANY KIND!
"""
def main():
    if len(sys.argv) == 2 and sys.argv[1] == "--example":
        example()
        return
    if len(sys.argv) == 2 and sys.argv[1] == "--docs":
        docs()
        return

    print("Enter absolute file paths (as long as possible). If you are referring to a file in the working directory, file name is enough.")
    if len(sys.argv) == 1:
        input_file_path = input("Enter input file: ")
    else:
        input_file_path = sys.argv[1]
    if len(sys.argv) > 2:
        output_file_path = sys.argv[2]
    else:
        output_file_path = input("Enter output file: ")
    convert(input_file_path, output_file_path)
    print("Translation finished!")
    webbrowser.open(output_file_path)

def convert(source, target):
    """
    Converts a file at @source location to a file at @target location. The source file is treated as Markdown formatted text file. The target file will be an HTML document.
    Returns the absolute path of the target file.
    """
    input_file_path = os.path.abspath(source)
    output_file_path = os.path.abspath(target)
    tokenizer = Tokenizer()
    parser = Parser()
    translator = Translator()
    markdown = Path(input_file_path).read_text()
    with open(output_file_path, "w") as output_file:
        output_file.write(translator.translate(parser.parse(tokenizer.tokenize(markdown))))
    return output_file_path
    
def example():
    output_file_path = convert(os.path.join("documents", "in.md"), os.path.join("documents", "out.html"))
    webbrowser.open(output_file_path)

def docs():
    output_file_path = convert(os.path.join("documents", "docs.md"), os.path.join("documents", "docs.html"))
    webbrowser.open(output_file_path)
        
if __name__ == "__main__":
    main()