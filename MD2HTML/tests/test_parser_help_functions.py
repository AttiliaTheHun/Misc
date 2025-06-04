import sys
import os
# Add parent directory to PATH because of imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(sys.argv[0]))))

from parser import Parser, Structure, Stack
from tokenizer import Token
import unittest

class ParserTest2(unittest.TestCase):


    def test_Parser__init(self):
        parser = Parser()
        super_structure = Structure([], Structure.Type.SUPER)
        
        parser._Parser__init()
        assert isinstance(parser.context_stack, Stack)
        assert isinstance(parser.token_buffer, list)
        assert len(parser.token_buffer) == 0
        assert parser.super_structure == super_structure
        assert parser.context_stack.get_last() == super_structure
        

    def test_Parser__parse_scope_independent(self):
        pass


    def test_Parser__is_line_empty__line_is_empty(self):
        parser = Parser()
        test_tokens = [[Token(" ", Token.Type.SPACE), Token(" ", Token.Type.SPACE), Token(" ", Token.Type.SPACE)], []]
            
        for i in range(len(test_tokens)):
            output = parser._Parser__is_line_empty(test_tokens[i])
            assert output == True, f"Failed to recognize an empty line for test {i+1}"
            
    def test_Parser__is_line_empty__line_not_empty(self):
        parser = Parser()
        test_tokens = [Token(" ", Token.Type.SPACE), Token(" ", Token.Type.SPACE), Token(" ", Token.Type.SPACE), Token("", Token.Type.TEXT)]
            
        output = parser._Parser__is_line_empty(test_tokens)
        assert output == False, f"Incorrectly found an empty line!"

    def test_Parser__is_hr_structure__is_hr_structure(self):
        parser = Parser()
        test_tokens = [[Token("**", Token.Type.ASTERISK), Token(" ", Token.Type.SPACE), Token("*", Token.Type.ASTERISK)],
            [Token(" ", Token.Type.SPACE), Token("", Token.Type.DASH), Token(" ", Token.Type.SPACE), Token("", Token.Type.DASH), Token(" ", Token.Type.SPACE), Token("", Token.Type.DASH),
            Token(" ", Token.Type.SPACE), Token("", Token.Type.DASH), Token(" ", Token.Type.SPACE), Token("", Token.Type.DASH)],
            [Token("___", Token.Type.UNDERSCORE)]]
            
        for i in range(len(test_tokens)):
            output = parser._Parser__is_hr_structure(test_tokens[i])
            assert output == True, f"Failed to recognize an hr structure for test {i+1}"
            
    def test_Parser__is_hr_structure__is_not_hr_structure(self):
        parser = Parser()
        test_tokens = [[Token("**", Token.Type.ASTERISK), Token("", Token.Type.DASH), Token("*", Token.Type.ASTERISK)],
            [Token(" ", Token.Type.SPACE), Token("", Token.Type.DASH), Token(" ", Token.Type.SPACE), Token("", Token.Type.DASH), Token(" ", Token.Type.SPACE), Token("", Token.Type.DASH),
            Token(" ", Token.Type.SPACE), Token("", Token.Type.DASH), Token(" ", Token.Type.SPACE), Token("lol", Token.Type.TEXT)],
            [Token("__", Token.Type.UNDERSCORE)],
            [Token("*", Token.Type.ASTERISK), Token("_", Token.Type.UNDERSCORE), Token("", Token.Type.DASH)]]
            
        for i in range(len(test_tokens)):
            output = parser._Parser__is_hr_structure(test_tokens[i])
            assert output == False, f"Incorrectly found and hr structure for test {i+1}"


    def test_Parser__push_to_buffer(self):
        parser = Parser()
        parser.token_buffer = [Token(" ", Token.Type.SPACE), Token("69", Token.Type.NUMBER)]
        token = Token("Peace", Token.Type.TEXT)
        
        assert len(parser.token_buffer) == 2, f"Something went wrong with the token buffer"
        parser._Parser__push_to_buffer(token)
        assert len(parser.token_buffer) == 3, f"Failed to push to the token buffer, the length is the same"
        assert parser.token_buffer[2] == token, f"Invalid token: {parser.token_buffer[2]} expected: {token}"

    def test_Parser__clear_buffer(self):
        parser = Parser()
        parser.token_buffer = [Token(" ", Token.Type.SPACE), Token("69", Token.Type.NUMBER)]
        
        assert len(parser.token_buffer) == 2, f"Something went wrong with the token buffer"
        parser._Parser__clear_buffer()
        assert len(parser.token_buffer) == 0, f"Failed to clear the token buffer!"

    def test_Parser__open_structure(self):
        """ TODO:  This test is incorrect """
        parser = Parser()
        parser._Parser__init()
        test_data = [(Structure.Type.HR, None), (Structure.Type.LINE_BREAK, Structure.Scope.PARAGRAPH), (Structure.Type.TEXT, Structure.Scope.CODE),
            (Structure.Type.ORDERED_LIST, Structure.Scope.BLOCKQUOTE), (Structure.Type.HEADING_3, Structure.Scope.LIST), (Structure.Type.STRONG, Structure.Scope.HEADING)]
        
        test_structures = [Structure([], Structure.Type.SUPER)]
        test_structures[0].content.append(Structure(None, Structure.Type.HR, test_structures[0], None))
        test_structures[0].content.append(Structure(None, Structure.Type.LINE_BREAK, test_structures[0], Structure.Scope.PARAGRAPH))
        test_structures.append(Structure("", Structure.Type.TEXT, test_structures[0], Structure.Scope.CODE))
        test_structures.append(Structure([], Structure.Type.ORDERED_LIST, test_structures[0], Structure.Scope.BLOCKQUOTE))
        test_structures.append(Structure([], Structure.Type.LIST_ITEM, test_structures[2], Structure.Scope.LIST))
        test_structures.append(Structure([], Structure.Type.HEADING_3, test_structures[3], Structure.Scope.LIST))
        test_structures.append(Structure([], Structure.Type.STRONG, test_structures[4], Structure.Scope.HEADING))
        test_structures = list(reversed(test_structures))
 
        for i in range(len(test_data)):
            parser._Parser__open_structure(test_data[i][0], test_data[i][1])
        print(f"{parser.context_stack.data}")
        for i in range(len(test_structures)):
            structure = parser.context_stack.poll()
            assert structure == test_structures[i], f"Incorrect structure is open: {structure} expected: {test_structures[i]} for test {i+1}"


    def test_Parser__open_recursively__should_not_open(self):
        types = [Structure.Type.PARAGRAPH, Structure.Type.CODEBLOCK, Structure.Type.CODE]
        tokens = [Token("", Token.Type.GT), Token(" ", Token.Type.SPACE), Token("texto", Token.Type.TEXT)]
        parser = Parser()
        parser._Parser__init()
        for i, kind in enumerate(types):
            parser._Parser__open_structure(kind, None)
            parser._Parser__open_recursively(tokens)
            structure = parser.context_stack.poll()
            assert structure.kind is kind, f"test {i+1} failed: {structure.kind} expected: {kind}"

    def test_Parser__open_recursively__should_open_blockquote(self):
        kind = Structure.Type.BLOCKQUOTE
        tokens = [Token("", Token.Type.GT), Token(" ", Token.Type.SPACE), Token("texto", Token.Type.TEXT)]
        parser = Parser()
        parser._Parser__init()

        index = parser._Parser__open_recursively(tokens)
        structure = parser.context_stack.poll()
        assert structure.kind is kind, f"test failed: {structure.kind} expected: {kind}"
        assert index == 2, f"test failed: {index} expected: {2}"

    def test_Parser__open_recursively__should_open_ordered_list(self):
        types = [Structure.Type.LIST_ITEM, Structure.Type.ORDERED_LIST]
        scopes = [Structure.Scope.LIST, None]
        tokens = [Token("4", Token.Type.NUMBER), Token("", Token.Type.PERIOD), Token(" ", Token.Type.SPACE), Token(" ", Token.Type.SPACE), Token("", Token.Type.GT), Token("texto", Token.Type.TEXT)]
        parser = Parser()
        parser._Parser__init()

        index = parser._Parser__open_recursively(tokens)
        for i in range(len(types)):
            structure = parser.context_stack.poll()
            assert structure.kind == types[i], f"test {i+1} failed: {structure.kind} expected: {types[i]}"
            assert structure.scope == scopes[i], f"test {i+1} failed: {structure.scope} expected: {scopes[i]}"
            assert index == 3, f"test {i+1} failed: {index} expected: {3}"

    def test_Parser__open_recursively__should_open_unordered_list__using_dashes(self):
        types = [Structure.Type.LIST_ITEM, Structure.Type.UNORDERED_LIST]
        scopes = [Structure.Scope.LIST, None]
        tokens = [Token("", Token.Type.DASH), Token(" ", Token.Type.SPACE), Token(" ", Token.Type.SPACE), Token("", Token.Type.GT), Token("texto", Token.Type.TEXT)]
        parser = Parser()
        parser._Parser__init()

        index = parser._Parser__open_recursively(tokens)
        for i in range(len(types)):
            structure = parser.context_stack.poll()
            assert structure.kind == types[i], f"test {i+1} failed: {structure.kind} expected: {types[i]}"
            assert structure.scope == scopes[i], f"test {i+1} failed: {structure.scope} expected: {scopes[i]}"
            assert index == 2, f"test {i+1} failed: {index} expected: {2}"

    def test_Parser__open_recursively__should_open_unordered_list__using_pluses(self):
        types = [Structure.Type.LIST_ITEM, Structure.Type.UNORDERED_LIST]
        scopes = [Structure.Scope.LIST, None]
        tokens = [Token("", Token.Type.PLUS), Token(" ", Token.Type.SPACE), Token(" ", Token.Type.SPACE), Token("", Token.Type.GT), Token("texto", Token.Type.TEXT)]
        parser = Parser()
        parser._Parser__init()

        index = parser._Parser__open_recursively(tokens)
        for i in range(len(types)):
            structure = parser.context_stack.poll()
            assert structure.kind == types[i], f"test {i+1} failed: {structure.kind} expected: {types[i]}"
            assert structure.scope == scopes[i], f"test {i+1} failed: {structure.scope} expected: {scopes[i]}"
            assert index == 2, f"test {i+1} failed: {index} expected: {2}"

    def test_Parser__open_recursively__should_open_unordered_list__using_asterisks(self):
        types = [Structure.Type.LIST_ITEM, Structure.Type.UNORDERED_LIST]
        scopes = [Structure.Scope.LIST, None]
        tokens = [Token("*", Token.Type.ASTERISK), Token(" ", Token.Type.SPACE), Token(" ", Token.Type.SPACE), Token("", Token.Type.GT), Token("texto", Token.Type.TEXT)]
        parser = Parser()
        parser._Parser__init()

        index = parser._Parser__open_recursively(tokens)
        for i in range(len(types)):
            structure = parser.context_stack.poll()
            assert structure.kind == types[i], f"test {i+1} failed: {structure.kind} expected: {types[i]}"
            assert structure.scope == scopes[i], f"test {i+1} failed: {structure.scope} expected: {scopes[i]}"
            assert index == 2, f"test {i+1} failed: {index} expected: {2}"


    def test_Parser__open_recursively__should_open_heading(self):
        kind = Structure.Type.HEADING_3
        tokens = [Token("###", Token.Type.HASH), Token(" ", Token.Type.SPACE), Token(" ", Token.Type.SPACE), Token(" ", Token.Type.SPACE), Token("", Token.Type.GT), Token("texto", Token.Type.TEXT)]
        parser = Parser()
        parser._Parser__init()

        index = parser._Parser__open_recursively(tokens)
        structure = parser.context_stack.poll()
        assert structure.kind == kind, f"test failed: {structure.kind} expected: {kind}"
        assert structure.scope == None, f"test failed: {structure.scope} expected: None"
        assert index == 2, f"test failed: {index} expected: {2}"

    def test_Parser__open_recursively__should_open_codeblock(self):
        types = [ Structure.Type.TEXT, Structure.Type.CODEBLOCK]
        scopes = [Structure.Scope.CODEBLOCK, None]
        tokens = [Token(" ", Token.Type.SPACE), Token(" ", Token.Type.SPACE), Token(" ", Token.Type.SPACE), Token(" ", Token.Type.SPACE), Token("", Token.Type.GT), Token("texto", Token.Type.TEXT)]
        parser = Parser()
        parser._Parser__init()

        index = parser._Parser__open_recursively(tokens)
        for i in range(len(types)):
            structure = parser.context_stack.poll()
            assert structure.kind == types[i], f"test {i+1} failed: {structure.kind} expected: {types[i]}"
            assert structure.scope == scopes[i], f"test {i+1} failed: {structure.scope} expected: {scopes[i]}"
            assert index == 4, f"test {i+1} failed: {index} expected: {4}"

    def test_Parser__open_recursively__should_open_paragraph(self):
        kind = Structure.Type.PARAGRAPH
        tokens = [[Token("", Token.Type.GT), Token("", Token.Type.GT), Token("texto", Token.Type.TEXT)],
                [Token(" ", Token.Type.SPACE), Token(" ", Token.Type.SPACE), Token("texto", Token.Type.TEXT)],
                [Token("##", Token.Type.HASH), Token("", Token.Type.GT), Token("texto", Token.Type.TEXT)],
                [Token("**", Token.Type.ASTERISK), Token(" ", Token.Type.SPACE), Token(" ", Token.Type.SPACE), Token("", Token.Type.GT), Token("texto", Token.Type.TEXT)]
        ]
        parser = Parser()
        parser._Parser__init()

        for i, t in enumerate(tokens):
            index = parser._Parser__open_recursively(t)
            structure = parser.context_stack.poll()
        assert structure.kind is kind, f"test {i+1} failed: {structure.kind} expected: {kind}"
        assert index == 0, f"test {i+1} failed: {index} expected: {0}"

    def test_Parser__finish_current_structure__should_inject_text_structure(self):
        parser = Parser()
        parser._Parser__init()
        tokens = [Token("Quite", Token.Type.TEXT), Token(" ", Token.Type.SPACE), Token("as", Token.Type.TEXT), Token(" ", Token.Type.SPACE), Token("good,", Token.Type.TEXT),
            Token(" ", Token.Type.SPACE), Token("as", Token.Type.TEXT), Token(" ", Token.Type.SPACE), Token("I", Token.Type.TEXT), Token(" ", Token.Type.SPACE), 
            Token("could", Token.Type.TEXT), Token(" ", Token.Type.SPACE), Token("have", Token.Type.TEXT)]
        parser.token_buffer = tokens
        string = "Quite as good, as I could have"
        structures = [Structure([], Structure.Type.PARAGRAPH, None, None)]
        structures.append(Structure([], Structure.Type.STRONG, structures[0], Structure.Scope.PARAGRAPH))
        endstate_structure = Structure([structures[1]], Structure.Type.PARAGRAPH, None, None)
        
        for structure in structures:
            parser.context_stack.push(structure)
        
        parser._Parser__finish_current_structure()
        top_structure = parser.context_stack.get_last()
        assert top_structure == endstate_structure, f"Structure finished incorrectly: {top_structure} expected end state: {endstate_structure}"
        assert top_structure.content[0].content[0].content == string, f"Incorrect content of the closed structure: {top_structure.content} expected: {string}"

    def test_Parser__finish_current_structure__should_not_inject_text_structure(self):
        parser = Parser()
        parser._Parser__init()
        tokens = [Token("Maybe", Token.Type.TEXT), Token(" ", Token.Type.SPACE), Token("I", Token.Type.TEXT), Token(" ", Token.Type.SPACE), Token("didn", Token.Type.TEXT),
            Token("", Token.Type.SINGLE_QUOTES), Token("t", Token.Type.TEXT), Token(" ", Token.Type.SPACE), Token("treat", Token.Type.TEXT), Token(" ", Token.Type.SPACE),
            Token("you", Token.Type.TEXT)]
        parser.token_buffer = tokens
        string = "Maybe I didn't treat you"
        structures = [Structure([], Structure.Type.PARAGRAPH, None, None)]
        structures.append(Structure("", Structure.Type.TEXT, structures[0], Structure.Scope.PARAGRAPH))
        endstate_structure = Structure([structures[1]], Structure.Type.PARAGRAPH, None, None)
        
        for structure in structures:
            parser.context_stack.push(structure)
        
        parser._Parser__finish_current_structure()
        top_structure = parser.context_stack.get_last()
        assert top_structure == endstate_structure, f"Structure finished incorrectly: {top_structure} expected end state: {endstate_structure}"
        assert top_structure.content[0].content == string, f"Incorrect content of the closed structure: {top_structure.content} expected: {string}"
        
    def test_Parser__finish_current_structure__buffer_is_empty(self):
        parser = Parser()
        parser._Parser__init()
        structures = [Structure([], Structure.Type.PARAGRAPH, None, None)]
        structures.append(Structure([], Structure.Type.EMPHASIS, structures[0], Structure.Scope.PARAGRAPH))
        endstate_structure = Structure([structures[1]], Structure.Type.PARAGRAPH, None, None)
        
        for structure in structures:
            parser.context_stack.push(structure)
        
        parser._Parser__finish_current_structure()
        top_structure = parser.context_stack.get_last()
        assert top_structure == endstate_structure, f"Structure finished incorrectly: {top_structure} expected end state: {endstate_structure}"

    def test_Parser__finish_structure(self):
        types = [Structure.Type.ORDERED_LIST, Structure.Type.BLOCKQUOTE, Structure.Type.BLOCKQUOTE, Structure.Type.HEADING_5, Structure.Type.EMPHASIS]
        scopes = [None, Structure.Scope.LIST, Structure.Scope.BLOCKQUOTE, Structure.Scope.BLOCKQUOTE, Structure.Scope.HEADING]
        test_type = Structure.Type.BLOCKQUOTE
        parser = Parser()
        parser._Parser__init()

        for i in range(len(types)):
            parser._Parser__open_structure(types[i], scopes[i])

        parser._Parser__finish_structure(test_type)

        assert len(parser.context_stack.data) == 4, f"Incorrect context stack length: {len(parser.context_stack.data)} expected: {4}"
        s = parser._Parser__get_scope_hierarchy()
        assert s == scopes[1:2], f"Incorrect scope hierarchy: {s} expected: {scopes[1:2]}"
        


    def test_Parser__finish_recursively__single_scope(self):
        types = [Structure.Type.ORDERED_LIST, Structure.Type.BLOCKQUOTE, Structure.Type.BLOCKQUOTE, Structure.Type.HEADING_5, Structure.Type.EMPHASIS]
        scopes = [None, Structure.Scope.LIST, Structure.Scope.BLOCKQUOTE, Structure.Scope.BLOCKQUOTE, Structure.Scope.HEADING]
        test_scopes = [Structure.Scope.HEADING]
        test_scope = Structure.Scope.BLOCKQUOTE
        test_structure = Structure([Structure([Structure([], Structure.Type.EMPHASIS)], Structure.Type.HEADING_5)], Structure.Type.BLOCKQUOTE)
        parser = Parser()
        parser._Parser__init()

        for i in range(len(types)):
            parser._Parser__open_structure(types[i], scopes[i])

        parser._Parser__finish_recursively(test_scopes)
        current_scope = parser._Parser__get_current_scope()
        structure = parser.context_stack.get_last()
        assert structure == test_structure, f"test failed: {structure} expected: {test_structure}"
        assert current_scope == test_scope, f"test failed: {current_scope} expected: {test_scope}"   

    def test_Parser__finish_recursively__nested_blockquote(self):
        types = [Structure.Type.ORDERED_LIST, Structure.Type.BLOCKQUOTE, Structure.Type.BLOCKQUOTE, Structure.Type.HEADING_5, Structure.Type.EMPHASIS]
        scopes = [None, Structure.Scope.LIST, Structure.Scope.BLOCKQUOTE, Structure.Scope.BLOCKQUOTE, Structure.Scope.HEADING]
        test_scopes = [Structure.Scope.HEADING, Structure.Scope.BLOCKQUOTE]
        test_scope = Structure.Scope.BLOCKQUOTE
        test_structure = Structure([Structure([Structure([Structure([], Structure.Type.EMPHASIS)], Structure.Type.HEADING_5)], Structure.Type.BLOCKQUOTE)], Structure.Type.BLOCKQUOTE)
        parser = Parser()
        parser._Parser__init()

        for i in range(len(types)):
            parser._Parser__open_structure(types[i], scopes[i])

        parser._Parser__finish_recursively(test_scopes)
        current_scope = parser._Parser__get_current_scope()
        structure = parser.context_stack.get_last()
        assert structure == test_structure, f"test failed: {structure} expected: {test_structure}"
        assert current_scope == test_scope, f"test failed: {current_scope} expected: {test_scope}" 

    def test_Parser__finish_recursively__double_blockquote(self):
        types = [Structure.Type.ORDERED_LIST, Structure.Type.BLOCKQUOTE, Structure.Type.BLOCKQUOTE, Structure.Type.HEADING_5, Structure.Type.EMPHASIS]
        scopes = [None, Structure.Scope.LIST, Structure.Scope.BLOCKQUOTE, Structure.Scope.BLOCKQUOTE, Structure.Scope.HEADING]
        test_scopes = [Structure.Scope.HEADING, Structure.Scope.BLOCKQUOTE, Structure.Scope.BLOCKQUOTE]
        test_scope = Structure.Scope.LIST
        test_structure = Structure([Structure([Structure([Structure([Structure([], Structure.Type.EMPHASIS)], Structure.Type.HEADING_5)], Structure.Type.BLOCKQUOTE)], Structure.Type.BLOCKQUOTE)], Structure.Type.LIST_ITEM)
        parser = Parser()
        parser._Parser__init()

        for i in range(len(types)):
            parser._Parser__open_structure(types[i], scopes[i])

        parser._Parser__finish_recursively(test_scopes)
        current_scope = parser._Parser__get_current_scope()
        structure = parser.context_stack.get_last()
        assert structure == test_structure, f"test failed: {structure} expected: {test_structure}"
        assert current_scope == test_scope, f"test failed: {current_scope} expected: {test_scope}" 
    
    def test_Parser__finish_recursively__is_false_positive__is_false_positive(self):
        parser = Parser()
        test_structures = [Structure([], Structure.Type.BLOCKQUOTE, None, Structure.Scope.BLOCKQUOTE), Structure([], Structure.Type.ORDERED_LIST, None, Structure.Scope.LIST),
            Structure([], Structure.Type.UNORDERED_LIST, None, Structure.Scope.LIST)]
        
        for i in range(len(test_structures)):
            output = parser._Parser__finish_recursively__is_false_positive(test_structures[i], test_structures[i].scope)
            assert output == True, f"False positive let slip: {test_structures[i]} for test {i+1}"
            
    def test_Parser__finish_recursively__is_false_positive__is_not_false_positive(self):
        parser = Parser()
        test_structures = [Structure([], Structure.Type.EMPHASIS, None, Structure.Scope.LIST), Structure([], Structure.Type.ORDERED_LIST, None, Structure.Scope.BLOCKQUOTE),
            Structure("", Structure.Type.TEXT, None, Structure.Scope.HEADING)]
        
        for i in range(len(test_structures)):
            output = parser._Parser__finish_recursively__is_false_positive(test_structures[i], test_structures[i].scope)
            assert output == False, f"False positive false positive: {test_structures[i]} for test {i+1}"
    
    
    def test_Parser__get_current_scope(self):
        parser = Parser()
        stack = Stack()
        stack.push(Structure([], Structure.Type.SUPER))
        test_output = [None, Structure.Scope.BLOCKQUOTE, Structure.Scope.PARAGRAPH, Structure.Scope.HEADING, Structure.Scope.HEADING, Structure.Scope.HEADING]
        parser.context_stack = stack
        
        for i in range(len(test_output)):
            match i:
                case 1:
                    stack.push(Structure([], Structure.Type.BLOCKQUOTE, stack.get_last()))
                case 2:
                    stack.push(Structure([], Structure.Type.PARAGRAPH, stack.get_last(), Structure.Scope.BLOCKQUOTE))
                case 3:
                    stack.push(Structure([], Structure.Type.HEADING_5, stack.get_last(), Structure.Scope.PARAGRAPH))
                case 4:
                    stack.push(Structure([], Structure.Type.EMPHASIS, stack.get_last(), Structure.Scope.HEADING))
                case 5:
                    stack.push(Structure("Wololo", Structure.Type.TEXT, stack.get_last(), Structure.Scope.HEADING))
            output = parser._Parser__get_current_scope()
            assert output == test_output[i], f"Got incorrect current scope: {output} expected: {test_output[i]} for test {i+1}"
    

    def test_Parser__get_scope_hierarchy(self):
        parser = Parser()
        stack = Stack()
        
        stack.push(Structure([], Structure.Type.SUPER))
        stack.push(Structure([], Structure.Type.BLOCKQUOTE, stack.get_last()))
        stack.push(Structure([], Structure.Type.PARAGRAPH, stack.get_last(), Structure.Scope.BLOCKQUOTE))
        stack.push(Structure([], Structure.Type.HEADING_5, stack.get_last(), Structure.Scope.PARAGRAPH))
        stack.push(Structure([], Structure.Type.EMPHASIS, stack.get_last(), Structure.Scope.HEADING))
        stack.push(Structure("Wololo", Structure.Type.TEXT, stack.get_last(), Structure.Scope.HEADING))
        
        test_output = [Structure.Scope.BLOCKQUOTE, Structure.Scope.PARAGRAPH, Structure.Scope.HEADING]
        parser.context_stack = stack
        
        output = parser._Parser__get_scope_hierarchy()
        assert output == test_output, f"Scope hierarchy creation failed: {output} expected: {test_output}"
    
    def test_Parser__get_open_structure(self):
        parser = Parser()
        stack = Stack()
        
        stack.push(Structure([], Structure.Type.SUPER))
        stack.push(Structure([], Structure.Type.BLOCKQUOTE, stack.get_last()))
        test_structure = stack.get_last()
        stack.push(Structure([], Structure.Type.PARAGRAPH, stack.get_last(), Structure.Scope.BLOCKQUOTE))
        stack.push(Structure([], Structure.Type.HEADING_5, stack.get_last(), Structure.Scope.PARAGRAPH))
        stack.push(Structure([], Structure.Type.EMPHASIS, stack.get_last(), Structure.Scope.HEADING))
        stack.push(Structure("Wololo", Structure.Type.TEXT, stack.get_last(), Structure.Scope.HEADING))
        
        parser.context_stack = stack
        
        output = parser._Parser__get_open_structure(Structure.Type.LIST_ITEM)
        assert output == None, f"Structure was found although it is not open: {output}"
        output = parser._Parser__get_open_structure(Structure.Type.BLOCKQUOTE)
        assert output == test_structure, f"Retrieved invalid scope chain: {output} expected: {test_structure}"
    
    def test_Parser__rstrip_tokens__should_strip(self):
        parser = Parser()
        test_tokens = [Token("", Token.Type.GT), Token(" ", Token.Type.SPACE), Token(" ", Token.Type.SPACE), Token(" ", Token.Type.SPACE)]
        test_output = 3
        
        output = parser._Parser__rstrip_tokens(test_tokens)
        assert output == test_output, f"Stripping tokens failed: {output} expected: {test_output}"
        
    def test_Parser__rstrip_tokens__should_not_strip(self):
        parser = Parser()
        test_tokens = [Token("", Token.Type.GT), Token(" ", Token.Type.SPACE), Token(" ", Token.Type.SPACE), Token("", Token.Type.LT)]
        test_output = 0
        
        output = parser._Parser__rstrip_tokens(test_tokens)
        assert output == test_output, f"Stripping tokens failed: {output} expected: {test_output}"
    
    
    def test_Parser__shift_by_scope__should_pass(self):
        parser = Parser()
        test_tokens = [Token("", Token.Type.GT), Token(" ", Token.Type.SPACE), Token("", Token.Type.GT), Token(" ", Token.Type.SPACE), Token("", Token.Type.DASH),
        Token(" ", Token.Type.SPACE), Token(" ", Token.Type.SPACE), Token(" ", Token.Type.SPACE), Token(" ", Token.Type.SPACE), Token(" ", Token.Type.SPACE), Token("Hello", Token.Type.TEXT),
        Token(" ", Token.Type.SPACE), Token("World", Token.Type.TEXT), Token("", Token.Type.EXCLAMATION_MARK)]
        test_scopes = [Structure.Scope.BLOCKQUOTE, Structure.Scope.BLOCKQUOTE, Structure.Scope.LIST, Structure.Scope.CODEBLOCK]
        test_outputs = [
            [Token("", Token.Type.GT), Token(" ", Token.Type.SPACE), Token("", Token.Type.DASH), Token(" ", Token.Type.SPACE), Token(" ", Token.Type.SPACE), Token(" ", Token.Type.SPACE),
            Token(" ", Token.Type.SPACE), Token(" ", Token.Type.SPACE), Token("Hello", Token.Type.TEXT), Token(" ", Token.Type.SPACE), Token("World", Token.Type.TEXT),
            Token("", Token.Type.EXCLAMATION_MARK)],
            [Token("", Token.Type.DASH), Token(" ", Token.Type.SPACE), Token(" ", Token.Type.SPACE), Token(" ", Token.Type.SPACE), Token(" ", Token.Type.SPACE), Token(" ", Token.Type.SPACE),
            Token("Hello", Token.Type.TEXT), Token(" ", Token.Type.SPACE), Token("World", Token.Type.TEXT), Token("", Token.Type.EXCLAMATION_MARK)],
            [Token(" ", Token.Type.SPACE), Token(" ", Token.Type.SPACE), Token(" ", Token.Type.SPACE), Token(" ", Token.Type.SPACE), Token("Hello", Token.Type.TEXT),
            Token(" ", Token.Type.SPACE), Token("World", Token.Type.TEXT), Token("", Token.Type.EXCLAMATION_MARK)],
            [Token("Hello", Token.Type.TEXT), Token(" ", Token.Type.SPACE), Token("World", Token.Type.TEXT), Token("", Token.Type.EXCLAMATION_MARK)]]
        
        output = test_tokens
        for i in range(len(test_scopes)):
            output = parser._Parser__shift_by_scope(output, test_scopes[i])
            assert len(output) == len(test_outputs[i])
            assert output == test_outputs[i], f"Shifting by scope failed: {output} expected: {test_outputs[i]} for test {i+1}"
       
    def test_Parser__shift_by_scope__should_fail(self):
        parser = Parser()
        test_tokens = [Token("Hello", Token.Type.TEXT), ("", Token.Type.SPACE), Token("World", Token.Type.TEXT), Token("", Token.Type.EXCLAMATION_MARK)]
        test_scope = Structure.Scope.BLOCKQUOTE
        test_output = False

        output = parser._Parser__shift_by_scope(test_tokens, test_scope)
        assert output == test_output, f"Shifting by scope failed: {output} expected: {test_output}"
    
    
    def test_Parser__stringify_tokens(self):
        parser = Parser()
        test_tokens = [Token("H", Token.Type.TEXT), Token("##", Token.Type.HASH), Token("l", Token.Type.TEXT), Token("", Token.Type.DASH),
            Token("lo", Token.Type.TEXT), Token("  ", Token.Type.SPACE), Token("", Token.Type.LBRACKET), Token("the", Token.Type.TEXT),
            Token("", Token.Type.RBRACE), Token("re", Token.Type.TEXT), Token("", Token.Type.EXCLAMATION_MARK), Token("*****", Token.Type.ASTERISK),
            Token("__", Token.Type.UNDERSCORE), Token("```", Token.Type.BACKTICK)]
        test_string = "H##l-lo  [the}re!*****__```"
        
        string = parser._Parser__stringify_tokens(test_tokens)
        assert test_string == string, f"Stringifying tokens failed: \"{string}\" expected: \"{test_string}\""
        
        
        
        
        
if __name__ == "__main__":
    unittest.main()
