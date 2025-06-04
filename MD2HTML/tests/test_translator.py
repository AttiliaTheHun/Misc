import sys
import os
# Add parent directory to PATH because of imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(sys.argv[0]))))

from translator import Translator
from parser import Structure
import unittest

class TranslatorTest(unittest.TestCase):
        
    def test_Translator__auto_escape(self):
        translator = Translator()
        
        test_input = "<html> is &almost a <language>"
        test_output = "&lt;html&gt; is &amp;almost a &lt;language&gt;"
        
        output = translator._Translator__auto_escape(test_input)
        
        assert test_output == output, f"Incorrectly escaped string { output } expected: { test_output }"
    
    
    def test_Translator__escape(self):
        translator = Translator()
        
        test_input = "<html&gt; is &almost &copy; a <language>"
        test_output = "&lt;html&gt; is &amp;almost &copy; a &lt;language&gt;"
        
        output = translator._Translator__escape(test_input)
        
        assert test_output == output, f"Incorrectly escaped string { output } expected: { test_output }"
    
    
    def test_Translator__translate_structure_1(self):
        translator = Translator()
        
        test_structure = Structure([Structure("One often meets\nhis ", Structure.Type.TEXT), Structure([Structure("destiny", Structure.Type.TEXT)], Structure.Type.EMPHASIS),
            Structure(" on the road ", Structure.Type.TEXT), Structure([Structure("he", Structure.Type.TEXT)], Structure.Type.STRONG), Structure("\ntakes to avoid it.", Structure.Type.TEXT)
            ], Structure.Type.PARAGRAPH)
        test_output = "<p>One often meets\nhis <em>destiny</em> on the road <strong>he</strong>\ntakes to avoid it.</p>"
        
        output = translator._Translator__translate_structure(test_structure)
        
        assert test_output == output, f"Incorrectly translated structure { output } expected: { test_output }"

    def test_Translator__translate_structure_2(self):
        translator = Translator()
        
        test_structure = Structure([Structure([Structure("public void main() {\n printf(\"C stoknks\");\n}", Structure.Type.TEXT)], Structure.Type.CODEBLOCK)
            ], Structure.Type.BLOCKQUOTE)
        test_output = "<blockquote><pre><code>public void main() {\n printf(\"C stoknks\");\n}</code></pre></blockquote>"
        
        output = translator._Translator__translate_structure(test_structure)
        
        assert test_output == output, f"Incorrectly translated structure { output } expected: { test_output }"

    def test_Translator__translate_structure_3(self):
        translator = Translator()
        
        test_structure = Structure([Structure([Structure([Structure("<span>Wololo</span>", Structure.Type.TEXT)], Structure.Type.HTML)], Structure.Type.LIST_ITEM),
            Structure([Structure("Text and ", Structure.Type.TEXT), Structure(None, Structure.Type.LINE_BREAK), Structure(" line break.", Structure.Type.TEXT)],
            Structure.Type.LIST_ITEM)
            ], Structure.Type.UNORDERED_LIST)
        test_output = "<ul><li><span>Wololo</span></li><li>Text and <br /> line break.</li></ul>"
        
        output = translator._Translator__translate_structure(test_structure)
        
        assert test_output == output, f"Incorrectly translated structure { output } expected: { test_output }"
    
    def test_Translator__translate_structure_4(self):
        translator = Translator()
        
        test_structure = Structure([Structure([Structure("<Message", Structure.Type.TEXT)], Structure.Type.LIST_ITEM),
            ], Structure.Type.ORDERED_LIST)
        test_output = "<ol><li>&lt;Message</li></ol>"
        
        output = translator._Translator__translate_structure(test_structure)
        
        assert test_output == output, f"Incorrectly translated structure { output } expected: { test_output }"
    
    def test_Translator__translate_structure_5(self):
        translator = Translator()
        
        test_structure = Structure(None, Structure.Type.HR)
        test_output = "<hr />"
        
        output = translator._Translator__translate_structure(test_structure)
        
        assert test_output == output, f"Incorrectly translated structure { output } expected: { test_output }"
    
    
    def test_Translator__translate_structure_6(self):
        translator = Translator()
        
        test_structure = Structure([Structure([Structure("Heading", Structure.Type.TEXT)], Structure.Type.HEADING_1), Structure([Structure("eading", Structure.Type.TEXT)],
            Structure.Type.HEADING_2), Structure([Structure("ading", Structure.Type.TEXT)], Structure.Type.HEADING_3),
            Structure([Structure("ding", Structure.Type.TEXT)], Structure.Type.HEADING_4), Structure([Structure("ing", Structure.Type.TEXT)], Structure.Type.HEADING_5),
            Structure([Structure("ngl", Structure.Type.TEXT)], Structure.Type.HEADING_6)
            ], Structure.Type.PARAGRAPH)
        test_output = "<p><h1>Heading</h1><h2>eading</h2><h3>ading</h3><h4>ding</h4><h5>ing</h5><h6>ngl</h6></p>"
        
        output = translator._Translator__translate_structure(test_structure)
        
        assert test_output == output, f"Incorrectly translated structure { output } expected: { test_output }"
    
    def test_Translator__translate_structure__escaping(self):
        translator = Translator()
        
        test_structure = Structure([Structure(" AT&T.\n&amp;", Structure.Type.TEXT), Structure([Structure(" AT&T., &amp;", Structure.Type.TEXT)], Structure.Type.CODE),
            Structure(None, Structure.Type.LINE_BREAK), Structure([Structure("<div>The mine is fake & lasers are real.</div>", Structure.Type.TEXT)], Structure.Type.HTML)
            ], Structure.Type.BLOCKQUOTE)
        test_output = "<blockquote> AT&amp;T.\n&amp;<code> AT&amp;T., &amp;amp;</code><br /><div>The mine is fake & lasers are real.</div></blockquote>"
        
        output = translator._Translator__translate_structure(test_structure)
        
        assert test_output == output, f"Incorrectly translated or escaped structure { output } expected: { test_output }"
    
    
    def test_Translator__translate(self):
        translator = Translator()
        
        test_structures = [Structure([Structure("Jim &amp; ", Structure.Type.TEXT), Structure([Structure("Carry", Structure.Type.TEXT)], Structure.Type.EMPHASIS)], Structure.Type.PARAGRAPH),
            Structure([Structure("John > Doe", Structure.Type.TEXT)], Structure.Type.HEADING_3), Structure([Structure("<div><span>k</span></div>", Structure.Type.TEXT)], Structure.Type.HTML)]
        test_output = "<p>Jim &amp; <em>Carry</em></p><h3>John &gt; Doe</h3><div><span>k</span></div>"
        
        output = translator.translate(test_structures)
        
        assert test_output == output, f"Incorrectly translated or escaped structures { output } expected: { test_output }"


if __name__ == "__main__":
    unittest.main()
