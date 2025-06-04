# MD2HTML Documentation
MD2HTML is a Markdown to HTML converter. The program takes a file with Markdown-formatted text and produces a file with the equivalent HTML-formatted text.

If you rather want to view this document as an HTML page in your browser, run the following command

     python main.py --docs


## Table of contents
1. Disclaimer
2. User Manual
3. Implemented and not implemented syntax
4. Conversion algorithm 
  1. Tokenization
  2. Parsing
  3. Translation
5. FAQs

*************

# 1. Disclaimer
This is a school project I took to finish my Programming classes, it is probably not suitable for deployment in production scenarios as it is not thoroughly tested. It may be useful to present a different approach than the use of regular expressions for the text format conversion problematic though.

# 2. User Manual
*Note: you need a working installation of the [Python programming language](https://www.python.org/) to be able to use this program.*

Using the following command will result in launching the program

     python main.py

The program will then ask for the path to the input file. The input file is your Markdown-formatted text file. You need to enter the path to this file in the terminal to proceed. The program next asks for the path of the output file. Now you need to enter the path of where you want the HTML-formatted text file to be created. After entering these paths, the program should say
    Translation finished!
and the process should be complete.

Keep in mind that you can use paths relative to the location from where you started the program. It is also possible to provide these paths as command-line arguments, which will look like this

     python main.py source.md target.html

where `source.md` is the Markdown file and `target.html` will be the output file.

To learn more about the Markdown format, [visit its official website](https://daringfireball.net/projects/markdown/). What part of the syntax mentioned there is implemented by this project is discussed in the next chapter.

For an example, you can have a look at the `documents/in.md` file. To see how this file will look like when converted, simply run the following command

     python main.py --example

# 3. Implemented and not implemented syntax
Markdown syntax has many features, some of which are not covered by this project. The ommited syntax includes

- Direct HTML elements or blocks of elements
- Multi-paragraph list items
- Specifying the `title` property of hyperlinks
- Images
- Set-ext style headings
- Hyperlink (and image) references
- Escaped e-mail addresses

The supported syntax rules are following:

- Escaped characters
- Paragraphs
- Blockquotes
- Ordered lists
- Unordered lists
- Codeblocks
- HTML character escape (into HTML entities)
- Emphasis
- Strong text
- Hyperlinks
- Atx-style headers
- Manual linebreaks
- Horizontal rules
- Inline code spans

To learn more about Markdown syntax visit [this page](https://daringfireball.net/projects/markdown/syntax).

# 4. Conversion algorithm
The program achieves the conversion in three subsequent steps:

1. The source text is converted into Markdown syntax tokens
2. The tokens are parsed line-by-line into general logic structures
3. These structures are converted into HTML code

The steps are handled in order by the following classes `Tokenizer` (inside tokenizer.py), `Parser` (inside parser.py) and `Translator` (indside translator.py).

## 1. Tokenization
In this step the entire text is converted into Markdown language tokens. A language token in this case is an instance of the `Token` class (inside tokenizer.py) and may look like this

    Token("**", Token.Type.ASTERISK)

Every character type that has a special meaning in markdown has its own token type. Other characters are simply bundled into a `Token.Type.TEXT` or `Token.Type.NUMBER` type of token. 
For a full ist of token types take a look at the tokenizer.py file.

As is demonstrated in the main.py file, the tokenization is handled by a `Tokenizer#tokenize(str)` call.

## 2. Parsing
Parsing in this case means the creation of structures from tokens. Structures are represented by the `Structure` class (inside parser.py). Structures always have a type and content, which means other structures.

The parsing can be done by a `Parser#parse(Token[][])` call.

### Block and inline structures
There are two types of structures, block structures:

- Lists
- Blockquotes
- Headings
- Codeblocks
- Paragraphs

and inline structures:

- Emphasis spans
- Strong spans
- Links
- Code spans

There is also a special structure `Structure.Type.TEXT` that is used to hold the actual text.

### The parsing process
The parser always processes a line worth of tokens at a time. It keeps the currently open structures in the order they were created on a context stack. It then goes through every line of tokens from the left and determines whether to close a structure or open a new one. Block structures are treated differently than inline structures.

#### Parsing block structures
Block structures are marked-up at the beginnning of the line and they can be nested into each other. The parser first checks if the currently block structures have their corresponding prefix on the line of tokens that is being process. We use the term *scope* here, which signifies the block structure as well as all its child structures (the structures inside this structure). This check is done by generating a list of open scopes at the context stack by the `Parser#__get_scope_hierarchy()` method and then trying to remove the prefix of each scope through the `Parser#__shift_by_scope(Token[], Structure.Scope)` method. If the removal fails, all scopes from there up are closed, meaning their structures and their inner structures are removed from the stack and embedded into the structure that is down below them on the stack.

#### Parsing inline structures
Next the parser tries to open new block sstructures by removing the remaining prefixes. That is the `Parser#__open_recursively(Token[])` method. After this is done, the rest of the text is parsed for inline structures by the `Parser#__parse_scope_independent(Token[])` method.


## 3. Translation
Finally the list of structures created by the parser needs to be translated into HTML. This is done recursively by converting each structure and its inner structures into HTML strings. The conversion 
usually means simply inserting the structure's stringifyied content into a pre-made HTML string in a look-up table. To learn more about this process, check the translator.py file. It is around 100 lines and pretty much self explanatory.

Translation can be done by calling `Translator#translate(Structure[])` method.

# 5. Frequently asked questions

## Why reinvent the wheel?
Although I know that projects of the same nature exist even for the same programming language, I believed I can learn a lot by creating a Markdown-to-HTML converter myself.

## Why not use regular expressions?
Regular expressions feel like cheating, but that is a bad answer if it makes the code efficient. The real reason is that they are very easy to get lost in and if they are not designed carfully, they can be very inefficient. I am not very fluent with regular expressions, so I decided to avoid them. I am aware that the [markdown2](https://github.com/trentm/python-markdown2) library uses them.