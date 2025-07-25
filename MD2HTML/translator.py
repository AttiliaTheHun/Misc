from parser import Structure

# TODO: images
# TODO: email escaping

class Translator:
    """
    The translator class can be used to translate the structures generated by a parser into an HTML markup.
    """
    
    # The HTML markup corresponding to each of the structures for easy lookup
    dictionary = {
        Structure.Type.HEADING_1: "<h1>%s</h1>",
        Structure.Type.HEADING_2: "<h2>%s</h2>",
        Structure.Type.HEADING_3: "<h3>%s</h3>",
        Structure.Type.HEADING_4: "<h4>%s</h4>",
        Structure.Type.HEADING_5: "<h5>%s</h5>",
        Structure.Type.HEADING_6: "<h6>%s</h6>",
        Structure.Type.EMPHASIS: "<em>%s</em>",
        Structure.Type.STRONG: "<strong>%s</strong>",
        Structure.Type.CODE: "<code>%s</code>",
        Structure.Type.CODEBLOCK: "<pre><code>%s</code></pre>",
        Structure.Type.BLOCKQUOTE: "<blockquote>%s</blockquote>",
        Structure.Type.PARAGRAPH: "<p>%s</p>",
        Structure.Type.ORDERED_LIST: "<ol>%s</ol>",
        Structure.Type.UNORDERED_LIST: "<ul>%s</ul>",
        Structure.Type.LIST_ITEM: "<li>%s</li>",
        Structure.Type.HR: "<hr />",
        Structure.Type.LINE_BREAK: "<br />",
    } 
            
    # HTML entities are characters they need to be escaped in a special manner, otherwise they will be rendered as a part of the markup
    # this dictionary maps each entity to its escaped form
    entities = {"&": "&amp;", ">": "&gt;", "<": "&lt;"}
    
    def __auto_escape(self, text):
        """
        Automaticaly escapes all HTML-problematic characters in the given @text.
        Returns a string.
        """
        if text is None:
            raise ValueError("cannot escape None")
        for key, value in self.entities.items():
            text = text.replace(key, value)
        return text
        
    def __escape(self, text):
        """
        Escapes HTML-problematic characters in the given @text. Ignores HTML entities.
        Returns a string.
        """
        if text is None:
            raise ValueError("cannot escape None")
        
        output = ""
        for i in range(len(text)):
            match text[i]:
                case "&":
                    index = text.find(";", i)
                    if index != -1 and text[i+1:index].isalpha():
                        output += text[i]
                    else:
                        output += self.entities["&"]
                case "<":
                    output += self.entities["<"]
                case ">":
                    output += self.entities[">"]
                case _:
                    output += text[i]
        return output

    def __escape_email(self, text):
        """ TODO """
        pass
        
    def translate(self, structures):
        """
        Translates a list of structures into HTML string. The structures are translated one-at-a-time and their inner structures are also translated. The translated structures
        are then concatenated to a single string. It is recommended to use an HTML formatting tool if you want the output to look good.
        Returns a string.
        """
        if structures is None:
            raise ValueError("cannot translate None")
        text = ""
        for structure in structures:
            text += self.__translate_structure(structure)
        return text
    
         
    def __translate_structure(self, structure):
        """
        Translates a single @structure into HTML string. The structure is translated recursively, if it contains other structures. The result string is escaped if necessary
        to ensure correct display when the HTML is rendered.
        Returns a string.
        """
        if structure.kind is Structure.Type.SUPER:
            raise ValueError("Unsupported structure type!")
        # These structures do not hold any content
        if structure.kind is Structure.Type.HR or structure.kind is Structure.Type.LINE_BREAK:
            return self.dictionary[structure.kind]
        if structure.content is None:
            raise ValueError("Structure content is None. Unexpected!")
        # HTML structures only ever contain a single TEXT structure with formatted HTML code
        if structure.kind is Structure.Type.HTML:
            return structure.content[0].content
        # Code structures only ever contain a single TEXT structure which needs to be specially escaped to not be potentially displayed as markup
        if structure.kind is Structure.Type.CODE or structure.kind is Structure.Type.CODEBLOCK:
            return self.dictionary[structure.kind].replace("%s", self.__auto_escape(structure.content[0].content))
        if structure.kind is Structure.Type.LINK:
            if structure.address is None or len(structure.address) == 0:
                structure.address = ""
            title = " title=" + structure.title + '"' if hasattr(structure, 'title') else ""
            text = f'<a href="{structure.address}"{title}>{self.__auto_escape(structure.content[0].content)}</a>'
            return text
        
        if structure.kind is Structure.Type.TEXT:
            return self.__escape(structure.content)
        # Structure contains other general structures
        text = ""
        for node in structure.content:
            text += self.__translate_structure(node)
        return self.dictionary[structure.kind].replace("%s", text)

