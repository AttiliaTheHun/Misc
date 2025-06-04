import sys
import os
# Add parent directory to PATH because of imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(sys.argv[0]))))

from parser import Parser, Structure
from tokenizer import Token
import unittest

class ParserTest(unittest.TestCase):
    
    def test_Parser_parse__parse_paragraph(self):
        self.parse_test_paragraphs()
        
    def test_Parser_parse__parse_codeblock(self):
        self.parse_test_codeblock()
        self.parse_test_codeblock_2()
        
    def test_Parser_parse__parse_blockquote(self):
        self.parse_test_blockquote()
        self.parse_test_blockquote_2()
        
    def test_Parser_parse__parse_ordered_list(self):
        self.parse_test_ordered_list()
        self.parse_test_ordered_list__multiline_items()
        #self.parse_test_ordered_list__multiparagraph_items()
        
    def test_Parser_parse__parse_unordered_list(self):
        self.parse_test_ordered_list()
        self.parse_test_ordered_list__multiline_items()
        
    def test_Parser_parse__parse_html_block(self):
        #self.parse_test_html_block()
        pass
        
    def test_Parser_parse__parse_emphasis(self):
        self.parse_test_emphasis()
        self.parse_test_emphasis_2()
        
    def test_Parser_parse__parse_strong(self):
        self.parse_test_strong()
        self.parse_test_strong_2()
        
    def test_Parser_parse__parse_atx_heading(self):
        self.parse_test_atx_heading()
        self.parse_test_atx_heading_2()
        
    def test_Parser_parse__parse_setext_heading(self):
        pass
        
    def test_Parser_parse__parse_inline_code(self):
        self.parse_test_inline_code()
        self.parse_test_inline_code_2()
        
    def test_Parser_parse__parse_image(self):
        pass
        
    def test_Parser_parse__parse_image_using_label(self):
        pass
        
    def test_Parser_parse__parse_link(self):
        self.parse_test_link()
        self.parse_test_link__should_not_parse()

    def test_Parser_parse__escapes(self):
        self.parse_test_escapes()
        self.parse_test_escapes_2()
        
    def test_Parser_parse__parse_link_using_label(self):
        pass
        
    def test_Parser_parse__parse_horizontal_rule(self):
        pass
        
    def test_Parser_parse__parse_blockquote_in_blockquote(self):
        pass
        
    def test_Parser_parse__parse_codeblock_in_unordered_list(self):
        pass
        
    def test_Parser_parse__parse_unordered_list_in_ordered_list(self):
        self.parse_test_unordered_list_in_ordered_list()

    def test_Parser_parse__absolute_destruction_tests(self):
        pass # test parsing ***bold* or italic** and then test all the shit nested together
        
        
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    def parse_test_link(self):
        parser = Parser()
        test_tokens = [[Token("Visit", Token.Type.TEXT),Token(" ", Token.Type.SPACE),  Token("", Token.Type.LBRACKET), Token("this", Token.Type.TEXT), Token(" ", Token.Type.SPACE),
            Token("link", Token.Type.TEXT), Token("", Token.Type.RBRACKET), Token("", Token.Type.LPAREN), Token("http", Token.Type.TEXT), Token("", Token.Type.COLON)],
            [Token("//example", Token.Type.TEXT), Token("", Token.Type.PERIOD), Token("com", Token.Type.TEXT),Token("", Token.Type.RPAREN), Token(" ", Token.Type.SPACE),
            Token("for", Token.Type.TEXT), Token(" ", Token.Type.SPACE), Token("more", Token.Type.TEXT), Token(" ", Token.Type.SPACE)], [ Token("information", Token.Type.TEXT),
            Token("", Token.Type.PERIOD)]]
        test_structure = Structure([Structure("Visit ", Structure.Type.TEXT),Structure([Structure("this link", Structure.Type.TEXT)], Structure.Type.LINK), Structure(" for more information.", Structure.Type.TEXT)], Structure.Type.PARAGRAPH)

        structures = parser.parse(test_tokens)

        assert 1 == len(structures), f"Incorrect number of parsed structures received: { len(structures) } expected: 1"
        assert test_structure == structures[0], f"Incorrect structure found: {structures[0]} expected: {test_structure}"
        assert structures[0].content[1].address == "http://example.com", f"Invalid link address found: {structures[0].content[1].address} expected: http://example.com"
    
    def parse_test_link__should_not_parse(self):
        parser = Parser()
        test_tokens = [[Token("Visit", Token.Type.TEXT),Token(" ", Token.Type.SPACE),  Token("", Token.Type.LBRACKET), Token("this", Token.Type.TEXT), Token(" ", Token.Type.SPACE),
            Token("link", Token.Type.TEXT), Token("", Token.Type.RBRACKET), Token("", Token.Type.LPAREN), Token("http", Token.Type.TEXT), Token("", Token.Type.COLON)],
            [Token("//example", Token.Type.TEXT), Token("", Token.Type.PERIOD), Token("com", Token.Type.TEXT), Token(" ", Token.Type.SPACE),
            Token("for", Token.Type.TEXT), Token(" ", Token.Type.SPACE), Token("more", Token.Type.TEXT), Token(" ", Token.Type.SPACE)], [ Token("information", Token.Type.TEXT),
            Token("", Token.Type.PERIOD)]]
        test_structure = Structure([Structure("Visit [this link](http://example.com for more information.", Structure.Type.TEXT)], Structure.Type.PARAGRAPH)

        structures = parser.parse(test_tokens)

        assert 1 == len(structures), f"Incorrect number of parsed structures received: { len(structures) } expected: 1"
        assert test_structure == structures[0], f"Incorrect structure found: {structures[0]} expected: {test_structure}"
        
    def parse_test_ordered_list(self):
        parser = Parser()
        test_tokens = [[Token("4", Token.Type.NUMBER),Token("", Token.Type.PERIOD),  Token(" ", Token.Type.SPACE), Token("Money", Token.Type.TEXT), Token(" ", Token.Type.SPACE)],
            [Token("1", Token.Type.NUMBER), Token("", Token.Type.PERIOD), Token(" ", Token.Type.SPACE), Token("Family", Token.Type.TEXT), Token(" ", Token.Type.SPACE)]]
        test_structure = Structure([Structure([Structure("Money ", Structure.Type.TEXT)], Structure.Type.LIST_ITEM), Structure([Structure("Family ", Structure.Type.TEXT)], Structure.Type.LIST_ITEM)], Structure.Type.ORDERED_LIST)
        
        structures = parser.parse(test_tokens)

        assert 1 == len(structures), f"Incorrect number of parsed structures received: { len(structures) } expected: 1"
        assert test_structure == structures[0], f"Incorrect structure found: {structures[0]} expected: {test_structure}"

    def parse_test_ordered_list__multiline_items(self):
        parser = Parser()
        test_tokens = [[Token("4", Token.Type.NUMBER),Token("", Token.Type.PERIOD),  Token(" ", Token.Type.SPACE), Token("Money", Token.Type.TEXT), Token(" ", Token.Type.SPACE)],
            [Token("aeternitas", Token.Type.TEXT)],
            [Token("1", Token.Type.NUMBER), Token("", Token.Type.PERIOD), Token(" ", Token.Type.SPACE), Token("Family", Token.Type.TEXT), Token(" ", Token.Type.SPACE)],
            [Token("temporandum", Token.Type.TEXT), ]]
        test_structure = Structure([Structure([Structure("Money aeternitas", Structure.Type.TEXT)], Structure.Type.LIST_ITEM), Structure([Structure("Family temporandum", Structure.Type.TEXT)], Structure.Type.LIST_ITEM)], Structure.Type.ORDERED_LIST)
        
        structures = parser.parse(test_tokens)

        assert 1 == len(structures), f"Incorrect number of parsed structures received: { len(structures) } expected: 1"
        assert test_structure == structures[0], f"Incorrect structure found: {structures[0]} expected: {test_structure}"

    def parse_test_ordered_list__multiparagraph_items(self):
        # TODO:
        parser = Parser()
        test_tokens = [[Token("4", Token.Type.NUMBER),Token("", Token.Type.PERIOD),  Token(" ", Token.Type.SPACE), Token("Money", Token.Type.TEXT), Token(" ", Token.Type.SPACE)],[],
            [Token(" ", Token.Type.SPACE), Token("aeternitas", Token.Type.TEXT)],[],
            [Token("1", Token.Type.NUMBER), Token("", Token.Type.PERIOD), Token(" ", Token.Type.SPACE), Token("Family", Token.Type.TEXT), Token(" ", Token.Type.SPACE)], [],
            [Token(" ", Token.Type.SPACE), Token("temporandum", Token.Type.TEXT) ], []]
        test_structure = Structure([Structure([Structure([Structure("Money ", Structure.Type.TEXT)], Structure.Type.PARAGRAPH), Structure([Structure("aeternitas", Structure.Type.TEXT)], Structure.Type.PARAGRAPH)],
            Structure.Type.LIST_ITEM), Structure([Structure([Structure("Family ", Structure.Type.TEXT)], Structure.Type.PARAGRAPH), Structure([Structure("temporandum", Structure.Type.TEXT)], Structure.Type.PARAGRAPH)],
            Structure.Type.LIST_ITEM)], Structure.Type.ORDERED_LIST)
        
        structures = parser.parse(test_tokens)

        assert 1 == len(structures), f"Incorrect number of parsed structures received: { len(structures) } expected: 1"
        assert test_structure == structures[0], f"Incorrect structure found: {structures[0]} expected: {test_structure}"
    
    def parse_test_unordered_list(self):
        parser = Parser()
        test_tokens = [[Token("*", Token.Type.ASTERISK),  Token(" ", Token.Type.SPACE), Token("Money", Token.Type.TEXT), Token(" ", Token.Type.SPACE)],
            [Token("", Token.Type.DASH), Token(" ", Token.Type.SPACE), Token("Family", Token.Type.TEXT), Token(" ", Token.Type.SPACE)]]
        test_structure = Structure([Structure([Structure("Money ", Structure.Type.TEXT)], Structure.Type.LIST_ITEM), Structure([Structure("Family ", Structure.Type.TEXT)], Structure.Type.LIST_ITEM)], Structure.Type.UNORDERED_LIST)
        
        structures = parser.parse(test_tokens)

        assert 1 == len(structures), f"Incorrect number of parsed structures received: { len(structures) } expected: 1"
        assert test_structure == structures[0], f"Incorrect structure found: {structures[0]} expected: {test_structure}"

    def parse_test_unordered_list__multiline_items(self):
        parser = Parser()
        test_tokens = [[Token("", Token.Type.PLUS), Token(" ", Token.Type.SPACE), Token("Money", Token.Type.TEXT), Token(" ", Token.Type.SPACE)],
            [Token("aeternitas", Token.Type.TEXT)],
            [Token("*", Token.Type.ASTERISK), Token(" ", Token.Type.SPACE), Token("Family", Token.Type.TEXT), Token(" ", Token.Type.SPACE)],
            [Token("temporandum", Token.Type.TEXT), ]]
        test_structure = Structure([Structure([Structure("Money aeternitas", Structure.Type.TEXT)], Structure.Type.LIST_ITEM), Structure([Structure("Family temporandum", Structure.Type.TEXT)], Structure.Type.LIST_ITEM)], Structure.Type.UNORDERED_LIST)
        
        structures = parser.parse(test_tokens)

        assert 1 == len(structures), f"Incorrect number of parsed structures received: { len(structures) } expected: 1"
        assert test_structure == structures[0], f"Incorrect structure found: {structures[0]} expected: {test_structure}"
        

    def parse_test_unordered_list_in_ordered_list(self):
        parser = Parser()
        test_tokens = [[Token("1", Token.Type.NUMBER),Token("", Token.Type.PERIOD),  Token(" ", Token.Type.SPACE), Token("Money", Token.Type.TEXT), Token(" ", Token.Type.SPACE)],
            [Token("  ", Token.Type.SPACE), Token("", Token.Type.DASH), Token(" ", Token.Type.SPACE), Token("Liberte", Token.Type.TEXT)],
            [Token("  ", Token.Type.SPACE), Token("", Token.Type.PLUS), Token(" ", Token.Type.SPACE), Token("Egalite", Token.Type.TEXT)],
            [Token("  ", Token.Type.SPACE), Token("*", Token.Type.ASTERISK), Token(" ", Token.Type.SPACE), Token("Fraterite", Token.Type.TEXT)],
            [Token("3", Token.Type.NUMBER),Token("", Token.Type.PERIOD),  Token(" ", Token.Type.SPACE), Token("Menthal", Token.Type.TEXT), Token(" ", Token.Type.SPACE), Token("health", Token.Type.TEXT)]]
        test_structure = Structure([Structure([Structure("Money ", Structure.Type.TEXT), Structure([Structure([Structure("Liberte", Structure.Type.TEXT)], Structure.Type.LIST_ITEM),
            Structure([Structure("Egalite", Structure.Type.TEXT)], Structure.Type.LIST_ITEM), Structure([Structure("Fraterite", Structure.Type.TEXT)], Structure.Type.LIST_ITEM)], Structure.Type.UNORDERED_LIST)],
            Structure.Type.LIST_ITEM), Structure([Structure("Menthal health", Structure.Type.TEXT)], Structure.Type.LIST_ITEM)], Structure.Type.ORDERED_LIST)
        
        structures = parser.parse(test_tokens)
        assert 1 == len(structures), f"Incorrect number of parsed structures received: { len(structures) } expected: 1"
        assert test_structure == structures[0], f"Incorrect structure found: {structures[0]} expected: {test_structure}"
    
    def parse_test_paragraphs(self):
        parser = Parser()
        test_tokens = [[Token("John", Token.Type.TEXT), Token(" ", Token.Type.SPACE), Token("Wick", Token.Type.TEXT), Token(".", Token.Type.PERIOD), Token(" ", Token.Type.SPACE)],
            [Token("Darth", Token.Type.TEXT), Token(" ", Token.Type.SPACE), Token("Vader", Token.Type.TEXT),
            Token("", Token.Type.PERIOD), Token(" ", Token.Type.SPACE)], [Token("K", Token.Type.TEXT)], [], [
            Token("Ethan", Token.Type.TEXT), Token(" ", Token.Type.SPACE), Token("Hunt", Token.Type.TEXT), Token("", Token.Type.PERIOD)]]
        test_structures = [Structure([Structure("John Wick. Darth Vader. K", Structure.Type.TEXT)], Structure.Type.PARAGRAPH),
            Structure([Structure("Ethan Hunt.", Structure.Type.TEXT)], Structure.Type.PARAGRAPH)]
        
        structures = parser.parse(test_tokens)

        assert len(test_structures) == len(structures), f"Incorrect number of parsed structures received: { len(structures) } expected: { len(test_structures) }"
        for i in range(len(test_structures)):
            assert test_structures[i] == structures[i], f"Incorrect structure found: {structures[i]} expected: {test_structures[i]} number {i}"
    
        
    def parse_test_codeblock(self):
        parser = Parser()
        test_tokens = [[Token("    ", Token.Type.SPACE),
            Token("Roses", Token.Type.TEXT), Token(" ", Token.Type.SPACE), Token("are", Token.Type.TEXT), Token(" ", Token.Type.SPACE),
            Token("red,", Token.Type.TEXT)], [Token("    ", Token.Type.SPACE), 
            Token("Violets", Token.Type.TEXT),
            Token(" ", Token.Type.SPACE), Token("are", Token.Type.TEXT), Token(" ", Token.Type.SPACE), Token(" ", Token.Type.SPACE),
            Token(" ", Token.Type.SPACE), Token("blue", Token.Type.TEXT), Token("", Token.Type.PERIOD)]]
        test_structures = [Structure([Structure("Roses are red,\nViolets are   blue.\n", Structure.Type.TEXT)], Structure.Type.CODEBLOCK)]

        structures = parser.parse(test_tokens)
        assert len(test_structures) == len(structures), f"Incorrect number of parsed structures received: { len(structures) } expected: { len(test_structures) }"
        for i in range(len(test_structures)):
            assert test_structures[i] == structures[i], f"Incorrect structure found: {structures[i]} expected: {test_structures[i]} number {i+1}"   
            
    def parse_test_codeblock_2(self):
        parser = Parser()
        test_tokens = [[Token("    ", Token.Type.SPACE),
            Token("1", Token.Type.NUMBER), Token("", Token.Type.PERIOD), Token(" ", Token.Type.SPACE), Token("`", Token.Type.BACKTICK), Token("~", Token.Type.TEXT),
            Token("", Token.Type.LT), Token("", Token.Type.GT), Token("***", Token.Type.ASTERISK)], [Token("    ", Token.Type.SPACE), 
            Token("", Token.Type.EQUALS)],[Token("    ", Token.Type.SPACE),
            Token("", Token.Type.GT), Token(" ", Token.Type.SPACE), Token("quote?", Token.Type.TEXT)]]
        test_structures = [Structure([Structure("1. `~<>***\n=\n> quote?\n", Structure.Type.TEXT)], Structure.Type.CODEBLOCK)]
        
        structures = parser.parse(test_tokens)
        assert len(test_structures) == len(structures), f"Incorrect number of parsed structures received: { len(structures) } expected: { len(test_structures) }"
        for i in range(len(test_structures)):
            assert test_structures[i] == structures[i], f"Incorrect structure found: {structures[i]} expected: {test_structures[i]} number {i}"
        pass
        
    def parse_test_blockquote(self):
        parser = Parser()
        test_tokens = [[Token("", Token.Type.GT), Token(" ", Token.Type.SPACE), Token("One", Token.Type.TEXT), Token(" ", Token.Type.SPACE),
            Token("often", Token.Type.TEXT), Token(" ", Token.Type.SPACE), Token("meets", Token.Type.TEXT), Token(" ", Token.Type.SPACE),
            Token("his", Token.Type.TEXT), Token(" ", Token.Type.SPACE), Token("destiny", Token.Type.TEXT), Token(" ", Token.Type.SPACE)],
            [Token("", Token.Type.GT), Token(" ", Token.Type.SPACE), Token("on", Token.Type.TEXT), Token(" ", Token.Type.SPACE),
            Token("the", Token.Type.TEXT), Token(" ", Token.Type.SPACE), Token("road", Token.Type.TEXT), Token(" ", Token.Type.SPACE),
            Token("he", Token.Type.TEXT), Token(" ", Token.Type.SPACE), Token("takes", Token.Type.TEXT),  Token(" ", Token.Type.SPACE)
            ], [Token("", Token.Type.GT), Token(" ", Token.Type.SPACE), Token("to", Token.Type.TEXT),
            Token(" ", Token.Type.SPACE), Token("avoid", Token.Type.TEXT), Token(" ", Token.Type.SPACE), Token("it", Token.Type.TEXT),
            Token("", Token.Type.PERIOD)]]
        test_structure = Structure([Structure("One often meets his destiny on the road he takes to avoid it.", Structure.Type.TEXT)], Structure.Type.BLOCKQUOTE)
        
        structures = parser.parse(test_tokens)

        assert 1 == len(structures), f"Incorrect number of parsed structures received: { len(structures) } expected: 1"
        assert test_structure == structures[0], f"Incorrect structure found: {structures[0]} expected: {test_structure}"

    def parse_test_blockquote_2(self):
        parser = Parser()
        test_tokens = [[Token("", Token.Type.GT), Token(" ", Token.Type.SPACE), Token("One", Token.Type.TEXT), Token(" ", Token.Type.SPACE),
            Token("often", Token.Type.TEXT), Token(" ", Token.Type.SPACE), Token("meets", Token.Type.TEXT), Token(" ", Token.Type.SPACE),
            Token("his", Token.Type.TEXT), Token(" ", Token.Type.SPACE), Token("destiny", Token.Type.TEXT), Token(" ", Token.Type.SPACE)],
            [Token("on", Token.Type.TEXT), Token(" ", Token.Type.SPACE),
            Token("the", Token.Type.TEXT), Token(" ", Token.Type.SPACE), Token("road", Token.Type.TEXT), Token(" ", Token.Type.SPACE),
            Token("he", Token.Type.TEXT), Token(" ", Token.Type.SPACE), Token("takes", Token.Type.TEXT), Token(" ", Token.Type.SPACE)
            ], [Token("to", Token.Type.TEXT),
            Token(" ", Token.Type.SPACE), Token("avoid", Token.Type.TEXT), Token(" ", Token.Type.SPACE), Token("it", Token.Type.TEXT),
            Token("", Token.Type.PERIOD)]]
        test_structure = Structure([Structure("One often meets his destiny on the road he takes to avoid it.", Structure.Type.TEXT)], Structure.Type.BLOCKQUOTE)
        
        structures = parser.parse(test_tokens)

        assert 1 == len(structures), f"Incorrect number of parsed structures received: { len(structures) } expected: 1"
        assert test_structure == structures[0], f"Incorrect structure found: {structures[0]} expected: {test_structure}"
        
    def parse_test_html_block(self):
        parser = Parser()
        tokens = [Token("", Token.Type.LT), Token("div", Token.Type.TEXT), Token("", Token.Type.GT), Token("", Token.Type.EOL),
            Token("", Token.Type.LT), Token("span", Token.Type.TEXT), Token("", Token.Type.GT), Token("ge", Token.Type.TEXT), Token(" ", Token.Type.SPACE),
            Token("Bob", Token.Type.TEXT), Token("", Token.Type.LT), Token("/span", Token.Type.TEXT), Token("", Token.Type.GT),
            Token("", Token.Type.EOL), Token("", Token.Type.LT), Token("/div", Token.Type.TEXT), Token("", Token.Type.GT), Token("", Token.Type.EOL),
            Token("", Token.Type.EOF)]
        test_structures = [Structure([Structure("<div><span>ge Bob</span></div>", Structure.Type.TEXT)], Stucture.Type.HTML)]
        structures = parser.parse(tokens)
        assert len(test_structures) == len(structures), f"Incorrect number of parsed structures received: { len(structures) } expected: { len(test_structures) }"
        for i in range(len(test_structures)):
            assert test_structures[i] == structures[i], f"Incorrect structure found: {structures[i]} expected: {test_structures[i]} number {i}"

    def parse_test_inline_code(self):
        parser = Parser()
        tokens = [[Token("Some", Token.Type.TEXT), Token(" ", Token.Type.SPACE), Token("text", Token.Type.TEXT), Token(" ", Token.Type.SPACE),
            Token("`", Token.Type.BACKTICK), Token("and", Token.Type.TEXT), Token(" ", Token.Type.SPACE), Token("some", Token.Type.TEXT),
            Token(" ", Token.Type.SPACE), Token("code", Token.Type.TEXT), Token("`", Token.Type.BACKTICK), Token(" ", Token.Type.SPACE),
            Token("and", Token.Type.TEXT), Token(" ", Token.Type.SPACE), Token("text", Token.Type.TEXT)]]
        test_structures = [Structure([Structure("Some text ", Structure.Type.TEXT), Structure([Structure("and some code", Structure.Type.TEXT)], Structure.Type.CODE), 
            Structure(" and text", Structure.Type.TEXT)], Structure.Type.PARAGRAPH)]
        structures = parser.parse(tokens)

        assert len(test_structures) == len(structures), f"Incorrect number of parsed structures received: { len(structures) } expected: { len(test_structures) }"
        for i in range(len(test_structures)):
            assert test_structures[i] == structures[i], f"Incorrect structure found: {structures[i]} expected: {test_structures[i]} number {i}"

    def parse_test_inline_code_2(self):
        parser = Parser()
        tokens = [[Token("Some", Token.Type.TEXT), Token(" ", Token.Type.SPACE), Token("text", Token.Type.TEXT), Token(" ", Token.Type.SPACE),
            Token("```", Token.Type.BACKTICK), Token("and", Token.Type.TEXT), Token(" ", Token.Type.SPACE), Token("some", Token.Type.TEXT),
            Token("`", Token.Type.BACKTICK), Token("code", Token.Type.TEXT), Token("```", Token.Type.BACKTICK), Token(" ", Token.Type.SPACE),
            Token("and", Token.Type.TEXT), Token(" ", Token.Type.SPACE), Token("text", Token.Type.TEXT)]]
        test_structures = [Structure([Structure("Some text ", Structure.Type.TEXT), Structure([Structure("and some`code", Structure.Type.TEXT)], Structure.Type.CODE), 
            Structure(" and text", Structure.Type.TEXT)], Structure.Type.PARAGRAPH)]
        structures = parser.parse(tokens)

        assert len(test_structures) == len(structures), f"Incorrect number of parsed structures received: { len(structures) } expected: { len(test_structures) }"
        for i in range(len(test_structures)):
            assert test_structures[i] == structures[i], f"Incorrect structure found: {structures[i]} expected: {test_structures[i]} number {i}"
        
    def parse_test_emphasis(self):
        parser = Parser()
        tokens = [[Token("Some", Token.Type.TEXT), Token(" ", Token.Type.SPACE), Token("text", Token.Type.TEXT), Token(" ", Token.Type.SPACE),
            Token("*", Token.Type.ASTERISK), Token("and", Token.Type.TEXT), Token(" ", Token.Type.SPACE), Token("some", Token.Type.TEXT),
            Token(" ", Token.Type.SPACE), Token("emp", Token.Type.TEXT), Token("*", Token.Type.ASTERISK), Token(" ", Token.Type.SPACE),
            Token("and", Token.Type.TEXT), Token(" ", Token.Type.SPACE), Token("text", Token.Type.TEXT)]]
        test_structures = [Structure([Structure("Some text ", Structure.Type.TEXT), Structure([Structure("and some emp", Structure.Type.TEXT)], Structure.Type.EMPHASIS), 
            Structure(" and text", Structure.Type.TEXT)], Structure.Type.PARAGRAPH)]
        structures = parser.parse(tokens)

        assert len(test_structures) == len(structures), f"Incorrect number of parsed structures received: { len(structures) } expected: { len(test_structures) }"
        for i in range(len(test_structures)):
            assert test_structures[i] == structures[i], f"Incorrect structure found: {structures[i]} expected: {test_structures[i]} number {i}"

    def parse_test_emphasis_2(self):
        parser = Parser()
        tokens = [[Token("Some", Token.Type.TEXT), Token(" ", Token.Type.SPACE), Token("text", Token.Type.TEXT), Token(" ", Token.Type.SPACE),
            Token("_", Token.Type.UNDERSCORE), Token("and", Token.Type.TEXT), Token(" ", Token.Type.SPACE), Token("some", Token.Type.TEXT),
            Token(" ", Token.Type.SPACE), Token("emp", Token.Type.TEXT), Token("_", Token.Type.UNDERSCORE), Token(" ", Token.Type.SPACE),
            Token("and", Token.Type.TEXT), Token(" ", Token.Type.SPACE), Token("text", Token.Type.TEXT)]]
        test_structures = [Structure([Structure("Some text ", Structure.Type.TEXT), Structure([Structure("and some emp", Structure.Type.TEXT)], Structure.Type.EMPHASIS), 
            Structure(" and text", Structure.Type.TEXT)], Structure.Type.PARAGRAPH)]
        structures = parser.parse(tokens)

        assert len(test_structures) == len(structures), f"Incorrect number of parsed structures received: { len(structures) } expected: { len(test_structures) }"
        for i in range(len(test_structures)):
            assert test_structures[i] == structures[i], f"Incorrect structure found: {structures[i]} expected: {test_structures[i]} number {i}"

    def parse_test_strong(self):
        parser = Parser()
        tokens = [[Token("Some", Token.Type.TEXT), Token(" ", Token.Type.SPACE), Token("text", Token.Type.TEXT), Token(" ", Token.Type.SPACE),
            Token("**", Token.Type.ASTERISK), Token("and", Token.Type.TEXT), Token(" ", Token.Type.SPACE), Token("some", Token.Type.TEXT),
            Token(" ", Token.Type.SPACE), Token("emp", Token.Type.TEXT), Token("**", Token.Type.ASTERISK), Token(" ", Token.Type.SPACE),
            Token("and", Token.Type.TEXT), Token(" ", Token.Type.SPACE), Token("text", Token.Type.TEXT)]]
        test_structures = [Structure([Structure("Some text ", Structure.Type.TEXT), Structure([Structure("and some emp", Structure.Type.TEXT)], Structure.Type.STRONG), 
            Structure(" and text", Structure.Type.TEXT)], Structure.Type.PARAGRAPH)]
        structures = parser.parse(tokens)

        assert len(test_structures) == len(structures), f"Incorrect number of parsed structures received: { len(structures) } expected: { len(test_structures) }"
        for i in range(len(test_structures)):
            assert test_structures[i] == structures[i], f"Incorrect structure found: {structures[i]} expected: {test_structures[i]} number {i}"

    def parse_test_strong_2(self):
        parser = Parser()
        tokens = [[Token("Some", Token.Type.TEXT), Token(" ", Token.Type.SPACE), Token("text", Token.Type.TEXT), Token(" ", Token.Type.SPACE),
            Token("__", Token.Type.UNDERSCORE), Token("and", Token.Type.TEXT), Token(" ", Token.Type.SPACE), Token("some", Token.Type.TEXT),
            Token(" ", Token.Type.SPACE), Token("emp", Token.Type.TEXT), Token("__", Token.Type.UNDERSCORE), Token(" ", Token.Type.SPACE),
            Token("and", Token.Type.TEXT), Token(" ", Token.Type.SPACE), Token("text", Token.Type.TEXT)]]
        test_structures = [Structure([Structure("Some text ", Structure.Type.TEXT), Structure([Structure("and some emp", Structure.Type.TEXT)], Structure.Type.STRONG), 
            Structure(" and text", Structure.Type.TEXT)], Structure.Type.PARAGRAPH)]
        structures = parser.parse(tokens)

        assert len(test_structures) == len(structures), f"Incorrect number of parsed structures received: { len(structures) } expected: { len(test_structures) }"
        for i in range(len(test_structures)):
            assert test_structures[i] == structures[i], f"Incorrect structure found: {structures[i]} expected: {test_structures[i]} number {i}"

    def parse_test_escapes(self):
        parser = Parser()
        tokens = [[Token("", Token.Type.BACKSLASH), Token("#", Token.Type.HASH), Token(" ", Token.Type.SPACE), Token("", Token.Type.BACKSLASH),
            Token("*", Token.Type.ASTERISK), Token("", Token.Type.BACKSLASH), Token("`", Token.Type.BACKTICK), Token("", Token.Type.BACKSLASH),
            Token("_", Token.Type.UNDERSCORE), Token("", Token.Type.BACKSLASH), Token("_", Token.Type.UNDERSCORE)]]
        test_structures = [Structure([Structure("# *`__", Structure.Type.TEXT)], Structure.Type.PARAGRAPH)]
        structures = parser.parse(tokens)

        assert len(test_structures) == len(structures), f"Incorrect number of parsed structures received: { len(structures) } expected: { len(test_structures) }"
        for i in range(len(test_structures)):
           assert test_structures[i] == structures[i], f"Incorrect structure found: {structures[i]} expected: {test_structures[i]} number {i}"

    def parse_test_escapes_2(self):
        parser = Parser()
        tokens = [[Token("", Token.Type.BACKSLASH), Token("", Token.Type.DASH), Token(" ", Token.Type.SPACE), Token("", Token.Type.BACKSLASH),
            Token("", Token.Type.LBRACKET), Token("legit", Token.Type.TEXT), Token("", Token.Type.RBRACKET), Token("", Token.Type.LPAREN),
            Token("http", Token.Type.TEXT), Token("", Token.Type.COLON), Token("//moeny", Token.Type.TEXT), Token("", Token.Type.PERIOD),
            Token("ru", Token.Type.TEXT), Token("", Token.Type.RPAREN)]]
        test_structures = [Structure([Structure("- [legit](http://moeny.ru)", Structure.Type.TEXT)], Structure.Type.PARAGRAPH)]
        structures = parser.parse(tokens)

        assert len(test_structures) == len(structures), f"Incorrect number of parsed structures received: { len(structures) } expected: { len(test_structures) }"
        for i in range(len(test_structures)):
           assert test_structures[i] == structures[i], f"Incorrect structure found: {structures[i]} expected: {test_structures[i]} number {i}"


    def parse_test_atx_heading(self):
        parser = Parser()
        tokens = [[ Token("###", Token.Type.HASH),  Token(" ", Token.Type.SPACE), Token("Glorious", Token.Type.TEXT), Token(" ", Token.Type.SPACE), 
            Token("and", Token.Type.TEXT), Token(" ", Token.Type.SPACE),
            Token("*", Token.Type.ASTERISK), Token("heading", Token.Type.TEXT), Token("*", Token.Type.ASTERISK),
            Token(" ", Token.Type.SPACE), Token("baby", Token.Type.TEXT), Token("", Token.Type.EXCLAMATION_MARK), Token(" ", Token.Type.SPACE)],
            [Token("Also", Token.Type.TEXT), Token(" ", Token.Type.SPACE), Token("text", Token.Type.TEXT)]]
        test_structures = [
            Structure([Structure("Glorious and ", Structure.Type.TEXT), Structure([Structure("heading", Structure.Type.TEXT)], Structure.Type.EMPHASIS), Structure(" baby! ", Structure.Type.TEXT)], Structure.Type.HEADING_3),
            Structure([Structure("Also text", Structure.Type.TEXT)], Structure.Type.PARAGRAPH)]
        structures = parser.parse(tokens)

        assert len(test_structures) == len(structures), f"Incorrect number of parsed structures received: { len(structures) } expected: { len(test_structures) }"        
        for i in range(len(test_structures)):
            assert test_structures[i] == structures[i], f"Incorrect structure found: {structures[i]} expected: {test_structures[i]} number {i}"

    def parse_test_atx_heading_2(self):
        parser = Parser()
        tokens = [[ Token("", Token.Type.GT), Token(" ", Token.Type.SPACE), Token("#", Token.Type.HASH),  Token(" ", Token.Type.SPACE), Token("Nested", Token.Type.TEXT), 
            Token(" ", Token.Type.SPACE), Token("guy", Token.Type.TEXT), Token(" ", Token.Type.SPACE), Token("##", Token.Type.HASH)]]
        test_structures = [Structure([Structure([Structure("Nested guy ", Structure.Type.TEXT)], Structure.Type.HEADING_1)], Structure.Type.BLOCKQUOTE)]
        structures = parser.parse(tokens)

        assert len(test_structures) == len(structures), f"Incorrect number of parsed structures received: { len(structures) } expected: { len(test_structures) }"
        for i in range(len(test_structures)):
            assert test_structures[i] == structures[i], f"Incorrect structure found: {structures[i]} expected: {test_structures[i]} number {i}"


        


        
if __name__ == "__main__":
    unittest.main()
