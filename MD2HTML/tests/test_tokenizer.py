import sys
import os
# Add parent directory to PATH because of imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(sys.argv[0]))))

from tokenizer import Tokenizer, Token
import unittest

class TokenizerTest(unittest.TestCase):

    def test_Tokenizer__finish_open_token(self):
        tokenizer = Tokenizer()
        test_string = "28##kl__**"
        test_tokens = [Token("28", Token.Type.NUMBER), Token("##", Token.Type.HASH), Token("kl", Token.Type.TEXT), Token("__", Token.Type.UNDERSCORE),
            Token("**", Token.Type.ASTERISK)]
        tokens = []
        assert (-1, None) == tokenizer._Tokenizer__finish_open_token(test_string, tokens, -1, None, 0)
        assert (-1, None) == tokenizer._Tokenizer__finish_open_token(test_string, tokens, 0, Token.Type.NUMBER, 2)
        assert (-1, None) == tokenizer._Tokenizer__finish_open_token(test_string, tokens, 2, Token.Type.HASH, 4)
        assert (-1, None) == tokenizer._Tokenizer__finish_open_token(test_string, tokens, 4, Token.Type.TEXT, 6)
        assert (-1, None) == tokenizer._Tokenizer__finish_open_token(test_string, tokens, 6, Token.Type.UNDERSCORE, 8)
        assert (-1, None) == tokenizer._Tokenizer__finish_open_token(test_string, tokens, 8, Token.Type.ASTERISK, 10)
        
        assert len(tokens) == len(test_tokens), f"incorrect number of elements - expected: {len(test_tokens)} actual: {len(tokens)}"
        for i in range(len(test_tokens)):
            if not test_tokens[i] == tokens[i]:
                raise AssertionError(f"expected token: {str(test_tokens[i])} actual: {str(tokens[i])} number {i}")
        
        
    def test_Tokenizer__tokenize_line(self):
        tokenizer = Tokenizer()
        test_string = ">\tword **Alice** ![  ](x){k}28"
        test_tokens = [Token("", Token.Type.GT), Token("    ", Token.Type.SPACE), Token("word", Token.Type.TEXT), Token(" ", Token.Type.SPACE),
            Token("**", Token.Type.ASTERISK), Token("Alice", Token.Type.TEXT), Token("**", Token.Type.ASTERISK),
            Token(" ", Token.Type.SPACE), Token("", Token.Type.EXCLAMATION_MARK), Token("", Token.Type.LBRACKET),
            Token("  ", Token.Type.SPACE), Token("", Token.Type.RBRACKET), Token("", Token.Type.LPAREN), Token("x", Token.Type.TEXT),
            Token("", Token.Type.RPAREN), Token("", Token.Type.LBRACE), Token("k", Token.Type.TEXT), Token("", Token.Type.RBRACE),
            Token("28", Token.Type.NUMBER)]
        tokens = []
        
        tokenizer._Tokenizer__tokenize_line(test_string, tokens)
        
        assert len(tokens) != 0, "the tokens seem not to be added to the target list"
        tokens = tokens[0]
        assert len(tokens) == len(test_tokens), f"incorrect number of elements - expected: {len(test_tokens)} actual: {len(tokens)}"
        for i in range(len(test_tokens)):
            if not test_tokens[i] == tokens[i]:
                raise AssertionError(f"expected token: {str(test_tokens[i])} actual: {str(tokens[i])} number {i}")
                
                
if __name__ == "__main__":
    unittest.main()
