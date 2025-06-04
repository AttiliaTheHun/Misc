from enum import Enum
from tokenizer import Token


class Structure:
    """
    This class represents a logical document structure such as list or a paragraph.
    """
    class Type(Enum):
        HEADING_1 = 0
        HEADING_2 = 1
        HEADING_3 = 2
        HEADING_4 = 3
        HEADING_5 = 4
        HEADING_6 = 5
        LINK = 6
        EMAIL = 7
        IMAGE = 8
        PARAGRAPH = 9
        BLOCKQUOTE = 10
        CODEBLOCK = 11
        EMPHASIS = 12
        STRONG = 13
        TEXT = 14
        HR = 15
        HTML = 16
        LINE_BREAK = 17
        SUPER = 18
        ORDERED_LIST = 19
        UNORDERED_LIST = 20
        CODE = 21
        LIST_ITEM = 22
        
        def __str__(self):
            return self.name
            
        def __repr__(self):
            return str(self)
    
    class Scope(Enum):
        PARAGRAPH = 0
        BLOCKQUOTE = 1
        LIST = 2
        CODEBLOCK = 3
        HTML = 4
        CODE = 5
        HEADING = 6
        
        def __str__(self):
            return self.name
            
        def __repr__(self):
            return str(self)
        
    def __init__(self, content, kind, parent=None, scope=None, metadata=[]):
        self.content = content
        self.kind = kind
        self.parent = parent
        self.scope = scope
        self.metadata = metadata
    
    
    def __eq__(self, other):
        if other is None:
            return False
        elif self.kind is not other.kind:
            return False
        elif self.content is None and other.content is None:
            return True
        elif self.content is None or other.content is None:
            return False
        elif len(self.content) != len(other.content):
            return False
        for i in range(len(self.content)):
            if self.content[i] != other.content[i]:
                return False
        return True
    
    
    def __str__(self):
        if isinstance(self.content, str):
            content = "'" + self.content + "'"
        elif self.content is None:
            content = "None"
        else:
            content = "["
            for x in self.content:
                content += str(x) + ", "
            if content.strip()[-1] == ",":
                content = content.strip()[:-1]
            content += "]"
        return f"{{ content: {content}, type: {str(self.kind)} }}"

    def __repr__(self):
        return str(self)

class Label:
    def __init__(data, title = ""):
        self.data = data
        self.title = title

class Stack:
    def __init__(self):
        self.data = []

    def push(self, value):
        self.data.append(value)
        
    def get_last(self):
        if len(self.data) == 0:
            return None
        return self.data[-1] 

    def poll(self):
        return self.data.pop()

class Parser:
    """
    This class is used to convert the tokens into logical structures.
    """
    def __init(self):
        self.super_structure = Structure([], Structure.Type.SUPER) # The parent structure for all other structures
        self.FLAG_LAST_LINE_EMPTY = False
        self.FLAG_IS_ESCAPED = False
        self.context_stack = Stack()
        self.context_stack.push(self.super_structure)
        self.token_buffer = [] # Stores tokens that are not yet part of any structure
        self.setext_heading_buffer = [] # Stores a line of tokens in case it is found to be a setext heading
        self.link_text_buffer = [] # Stores tokens that will possibly hold the textual part of a LINK
        self.link_address_buffer = [] # Stores tokens that will possibly hold the address of a LINK
        self.link_title_buffer = [] # Stores tokens that will possibly hold the title of a LINK
        self.link_buffer_stage = 0 # Stage 1 is buffering the text, stage 2 is buffering the address
        self.link_data_buffer_index = -1 # Holds the index in the token_buffer from where on the tokens are being buffered for link recognition so that the buffer can be cut to this index
    
    def parse(self, tokens):
        """
        Parses a list of token lists into a list of structures.
        Returns a list of {@link Structure}
        """
        self.__init()
        for line in tokens:
            self.__parse_line(line)

        open_scopes = self.__get_scope_hierarchy()
        if len(open_scopes) != 0:
            self.__finish_recursively(open_scopes)

        return self.super_structure.content
    
    def __parse_line(self, tokens):
        open_scopes = self.__get_scope_hierarchy()

        if self.__is_line_empty(tokens):
            self.FLAG_LAST_LINE_EMPTY = True
            if True:
                if len(open_scopes) != 0:
                    self.__finish_recursively(open_scopes)
            return
        
        
        # We first need to check which scopes are no longer open (structures that have been closed) and eventually close them
        # We also remove the prefixes of these scopes from the tokens
        list_scopes_count = sum(1 for scope in open_scopes if scope is Structure.Scope.LIST) # Total number of open list scopes
        for i, scope in enumerate(open_scopes):
            HAS_NESTED_LISTS = False
            if scope is Structure.Scope.LIST:
                HAS_NESTED_LISTS = list_scopes_count > 1
                list_scopes_count -= 1
            shifted_tokens = self.__shift_by_scope(tokens, scope, HAS_NESTED_LISTS)
            
            if shifted_tokens is False:
                if HAS_NESTED_LISTS is True:
                    # Returning False when HAS_NESTED_LISTS is True signals us to close all upcomming scopes to avoid adding items to the wrong list
                    self.__finish_recursively(open_scopes[i+1:])
                    tokens = self.__shift_by_scope(tokens, Structure.Scope.LIST) # We still need to remove the prefix, otherwise it starts a new list
                else:
                    self.__finish_recursively(open_scopes[i:])
                break
            else:
                tokens = shifted_tokens
        # Next we check the structures that occupy the entire line of tokens
        if self.__is_hr_structure(tokens):
            self.__open_structure(Structure.Type.HR)
            return
        if (level := self.__is_setext_underline(tokens)) == -1:
            self.setext_heading_buffer = tokens
        else:
            pass
        
        # Finally we parse what is left of the tokens to first open new block scopes and then parse the rest into inline sturctures
        index = self.__open_recursively(tokens.copy())
        self.__parse(tokens[index:])
        self.FLAG_LAST_LINE_EMPTY = False
            
       
 
        
    def __parse(self, tokens):
        """
        Parses a list of tokens in to inline-level structures. Modifies the @tokens list.
        """
        scope = self.__get_current_scope()
        match scope:
            case Structure.Scope.CODEBLOCK:
                # Codeblock is a block level structure, it can not be closed from this line
                # Moreover, text inside codeblocks is not evaluated
                self.__push_to_buffer(tokens)
                self.__push_to_buffer(Token("", Token.Type.EOL)) # Codeblocks have hardcoded ends-of-line
            case Structure.Scope.CODE:
                # Text marked as code is not evaluated. Inline code is closed by a backtick token.
                for i in range(len(tokens)):
                    if tokens[i].kind is Token.Type.BACKTICK and tokens[i] == self.context_stack.get_last().metadata[0]:
                        self.__finish_current_structure()
                        self.__parse_scope_independent(tokens[i:]) # Parse the rest of the tokens
                    else:
                        self.__push_to_buffer(token)
            case Structure.Scope.HTML:
                # HTML blocks are not processed
                self.__push_to_buffer(tokens)
            case Structure.Scope.HEADING:
                heading_level = len(self.context_stack.get_last().metadata[0].value)
                # atx-style headings are allowed to be closed with an arbitrary number of hash signs (a HASH token)
                # these need to be removed
                trail_spaces = self.__rstrip_tokens(tokens) # Remove any spaces at the end of the line
                if tokens[-1].kind is Token.Type.HASH:
                    tokens.pop()
                tokens.append(Token(" " * trail_spaces, Token.Type.SPACE))# We need to put the spaces back, because __parse_scope_independent() is meant to handle them 
                self.__parse_scope_independent(tokens)
                # Headings are not allowed to span more than a single line, so at the end of the parsing, we need to close the heading
                self.__finish_structure(Structure.Type[f"HEADING_{heading_level}"])
            case _:  
                # PARAGRAPH, LIST, BLOCKQUOTE
                self.__parse_scope_independent(tokens)
                    
    
    def __parse_scope_independent(self, tokens):
        trail_spaces = self.__rstrip_tokens(tokens)
        scope = self.__get_current_scope()
        
        for i, token in enumerate(tokens):
            # When parsing CODE, the markup is not being evaluated
            if scope is Structure.Scope.CODE:
                if token.kind is Token.Type.BACKTICK and token == self.context_stack.get_last().metadata[0]:
                    self.__finish_current_structure()
                    scope = self.__get_current_scope()
                else:
                    self.__push_to_buffer(token)
                continue
            
            if self.FLAG_IS_ESCAPED is True:
                self.FLAG_IS_ESCAPED = False
                # Only certain token types can be escaped
                if token.kind in Token.escapable_tokens:
                    # Only the first symbol in multicharacter tokens is escaped
                    if len(token.value) > 1:
                       self.__push_to_buffer(Token(token.value[0]), token.kind)
                       token.value = token.value[1:] 
                    else:
                        self.__push_to_buffer(token)
                        continue
                else:
                    # If we did not escape, we need to reintroduced the backslash back to the text
                    self.__push_to_buffer(Token("", Token.Type.BACKSLASH))

            # Flag escape if encountered a backslash
            if token.kind is Token.Type.BACKSLASH and i < len(tokens):
                self.FLAG_IS_ESCAPED = True
                continue
                

            match token.kind:
                case Token.Type.ASTERISK | Token.Type.UNDERSCORE:
                    if len(token.value) == 1:
                        open_em = self.__get_open_structure(Structure.Type.EMPHASIS)                        
                        if open_em is not None and (i != 0 and tokens[i-1].kind is not Token.Type.SPACE) and token == open_em.metadata[0]:
                            self.__finish_structure(Structure.Type.EMPHASIS)
                        elif i+1 != len(tokens) and tokens[i+1].kind is not Token.Type.SPACE:
                            self.__open_structure(Structure.Type.EMPHASIS, scope, [token])
                    elif len(token.value) == 2:
                        open_st = self.__get_open_structure(Structure.Type.STRONG)
                        if open_st is not None and (i != 0 and tokens[i-1].kind is not Token.Type.SPACE) and token == open_st.metadata[0]:
                            self.__finish_structure(Structure.Type.STRONG)
                        elif i+1 != len(tokens) and tokens[i+1].kind is not Token.Type.SPACE:
                            self.__open_structure(Structure.Type.STRONG, scope, [token])
                case Token.Type.LBRACKET:
                    if self.link_buffer_stage == 0:
                        self.link_buffer_stage = 1
                        self.link_data_buffer_index = len(self.token_buffer)
                    self.__push_to_buffer(token)
                case Token.Type.RBRACKET:
                    if self.link_buffer_stage == 1:
                        self.link_buffer_stage = 0
                    self.__push_to_buffer(token)
                case Token.Type.LPAREN:
                    if self.link_buffer_stage == 0 and len(self.link_text_buffer) != 0:
                        self.link_buffer_stage = 2
                    self.__push_to_buffer(token)
                case Token.Type.RPAREN:
                    if self.link_buffer_stage == 2:
                        self.__create_link()
                    else:
                        self.__push_to_buffer(token)
                #case Token.Type.LT:
                #    pass
                #case Token.Type.GT:
                #    pass
                case Token.Type.BACKTICK:
                    self.__open_structure(Structure.Type.CODE, scope, [token])
                    scope = self.__get_current_scope()
                #case Token.Type.EXCALAMATION_MARK:
                    #pass
                case _:
                    self.__push_to_buffer(token)
                    self.__push_to_link_buffer(token)

        # image

        # Two spaces at the end of the line can be used to trigger a manual linebreak, this is only applicable in certain contexts though.
        if trail_spaces >= 2 and self.__get_current_scope() in [Structure.Scope.PARAGRAPH, Structure.Scope.BLOCKQUOTE, Structure.Scope.LIST]:
            self.__open_structure(Structure.Type.LINE_BREAK, self.__get_current_scope())
        elif trail_spaces == 1:
            self.__push_to_buffer(Token(" ", Token.Type.SPACE))

        
    def __is_line_empty(self, tokens):
        """
        Checks whether @tokens contains any other tokens than spaces.
        Returns boolean.
        """
        for token in tokens:
            if token.kind is not Token.Type.SPACE:
                return False
        return True
        
    def __is_hr_structure(self, tokens):
        """
        Checks whether @tokens represent a horizontal rule structure.
        Returns boolean.
        """
        # Three or more characters of the same type from DASHES, ASTERISKS and UNDERSCORES make a horizontal rule
        # These characters can not be mixed with any other, but may contain spaces in between them
        quantities = [0, 0, 0]
        for token in tokens:
            match token.kind:
                case Token.Type.SPACE:
                    continue
                case Token.Type.DASH:
                    quantities[0] += 1
                case Token.Type.ASTERISK:
                    quantities[1] += len(token.value) # ASTERISK tokens may represent multiple asterisks
                case Token.Type.UNDERSCORE:
                    quantities[2] += len(token.value) # UNDERSCORE tokens may represent multiple underscores
                case _:
                    return False
        # If only the allowed characters are present, but more than a single type was used, it is not a valid horizontal rule       
        sumq = sum(quantities)
        if sumq < 3:
            return False
        for i in quantities:
            if sumq == i and i != 0:
                return True
        return False
    
    def __is_setext_underline(self, tokens):
        """
        Looks through a list of @tokens and determines whether they represent a setext heading underline.
        Returns
                a) 1 if it is a heading level 1 underline
                b) 2 if it is a heading level 2 underline
                c) -1 if it is not a setext heading underline
        """
        if len(tokens) == 0:
            return -1
        if tokens[0].kind is Token.Type.EQUALS:
            heading_level = 1 
        elif tokens[0].kind is Token.Type.DASH:
            heading_level = 2
        else:
            return -1
        for token in tokens:
            if not ((heading_level == 1 and token.kind is Token.Type.EQUALS) or (heading_level == 2 and token.kind is Token.Type.DASH)):
                return -1
        return heading_level
    
    def __push_to_buffer(self, token):
        """
        Adds @token to the inner token buffer.
        """
        if isinstance(token, list):
            self.token_buffer += token
        else: 
            self.token_buffer.append(token)
    
    
    def __clear_buffer(self):
        """
        Clears the inner token buffer of the parser.
        """
        self.token_buffer.clear()
    
    def __push_to_link_buffer(self, token):
        """
        Adds @token to the corresponding buffer for link-parsing data based upod the current link_buffer_stage. If the stage is 0, the token is discarded.
        """
        if self.link_buffer_stage == 0:
            return
        if self.link_buffer_stage == 1:
            buffer = self.link_text_buffer
        elif self.link_buffer_stage == 2:
            buffer = self.link_address_buffer
        if isinstance(token, list):
            buffer += token
        else: 
            buffer.append(token)

    def __reset_link_metadata(self):
        """
        Sets the inner data fields related to parsing links to their default state.
        """
        self.link_text_buffer = []
        self.link_address_buffer = []
        self.link_title_buffer = []
        self.link_data_buffer_index = -1
        self.link_buffer_stage = 0

    def __create_link(self):
        """
        Opens a LINK structure from the inner stored data and then finishes the structure, effectively creating a LINK in the parent structure.
        """
        self.token_buffer = self.token_buffer[:self.link_data_buffer_index]
        self.__open_structure(Structure.Type.LINK) # This should save and empty the token_buffer
        self.context_stack.get_last().address = self.__stringify_tokens(self.link_address_buffer)
        self.__push_to_buffer(self.link_text_buffer)
        self.__finish_current_structure() # This should save the token_buffer as a TEXT structure inside the LINK structure we opened
        self.__reset_link_metadata()

    def __wrap_top_text_in_paragraph(self):
        # TODO:
        structure = self.context_stack.get_last()
        if structure.kind is Structure.Type.TEXT:
            if structure.parent is None:
                return
            if tructure.parent.kind is Structure.Type.PARAGRAPH:
                self.__finish_structure(Structure.Type.PARAGRAPH)
            else:
                paragraph = Structure([], Structure.Type.PARAGRAPH, structure.parent, structure.scope)
                structure.parent.content.append(paragraph)
                structure.parent = paragraph
                return
        if structure.kind is Structure.Type.PARAGRAPH:
            self.__finish_current_structure()
        self.__open_structure(Structure.Type.PARAGRAPH)
        self.__open_structure(Structure.Type.TEXT)
        pass

    def __open_structure(self, kind, scope=None, metadata=[]):
        """
        Pushes a structure of specific type (@kind) and @scope with empty content to the context stack.
        """
        if scope is None:
            scope = self.__get_current_scope()
        # Opening a structure usually means changing scope, so we need to reset the metadata gathered for links
        if kind is not Structure.Type.LINK and self.link_buffer_stage != 1:
            self.__reset_link_metadata()
        top_structure = self.context_stack.get_last()
        # If we are opening a TEXT structure when a TEXT structure is open, we will merge them (do nothing and their buffers will merge)
        if top_structure.kind is Structure.Type.TEXT and kind is Structure.Type.TEXT:
            return
        # TEXT structure can not contain other structures. Its purpose is to wrap text.
        if kind is Structure.Type.TEXT:
            self.context_stack.push(Structure("", kind, top_structure, scope, metadata))
            return
        # If the current open structure is TEXT, we need to close it, because TEXT cannot contain other structures
        if top_structure.kind is Structure.Type.TEXT:
            self.__finish_current_structure()
            top_structure = self.context_stack.get_last()
        # If we are opening a non-TEXT structure and the token buffer was not saved into a previous TEXT structure, we will create a new TEXT structure to preserve the data
        # in the buffer and then we continue with opening whatever we are supposed to open
        if len(self.token_buffer) > 0:
            self.context_stack.push(Structure("", Structure.Type.TEXT, top_structure, scope))
            self.__finish_current_structure()
            top_structure = self.context_stack.get_last()
        # HR and LINE_BREAK can not hold any kind of content, so there is no "opening" these structures  
        if kind in [Structure.Type.HR, Structure.Type.LINE_BREAK]:
            top_structure.content.append(Structure(None, kind, top_structure, scope, metadata)) 
        # All content of any kind of list must be inside a LIST_ITEM structure, so we can as well open a LIST_ITEM when we open a list
        elif kind in [Structure.Type.ORDERED_LIST, Structure.Type.UNORDERED_LIST]:
            self.context_stack.push(Structure([], kind, top_structure, scope, metadata))
            top_structure = self.context_stack.get_last()
            self.context_stack.push(Structure([], Structure.Type.LIST_ITEM, top_structure, Structure.Scope.LIST, metadata))
        else:
            self.context_stack.push(Structure([], kind, top_structure, scope, metadata))
        
    def __open_recursively(self, tokens):
        """
        Goes through @tokens from the left and when possible, opens a block-level structure on the stack. The function destroys the list @tokens, 
        make sure you pass a copy of the actual data! When there are no more block-level structures to open, the function returns the number of 
        tokens it has parsed. This number can used as an index in the original data list.
        Returns integer.
        """
        scope = self.__get_current_scope()
        if scope in [Structure.Scope.PARAGRAPH, Structure.Scope.CODEBLOCK, Structure.Scope.CODE]:
            return 0 # There can be no other block-level structures in these scopes
            
        if len(tokens) > 2 and tokens[0].kind is Token.Type.GT and tokens[1].kind is Token.Type.SPACE:
            self.__open_structure(Structure.Type.BLOCKQUOTE, scope)
            return self.__open_recursively(tokens[2:]) + 2
        
        if len(tokens) > 2:
            if tokens[0].kind is Token.Type.SPACE and len(tokens[0].value) >= 4:
                self.__open_structure(Structure.Type.CODEBLOCK, scope)
                # The actual code will be stored in a text structure
                self.__open_structure(Structure.Type.TEXT, Structure.Scope.CODEBLOCK)
                if len(tokens[0].value) == 4:
                    return self.__open_recursively(tokens[1:]) + 1
                else:
                    tokens[0].value = tokens[0].value[4:]
                    return self.__open_recursively(tokens) + 0

        # Because ASTERISK tokens can represent multiple asterisks, we have to filter out the single character one
        if len(tokens) > 2 and (tokens[0].kind in [Token.Type.DASH, Token.Type.PLUS] or tokens[0].value == "*") and tokens[1].kind is Token.Type.SPACE:
            self.__open_structure(Structure.Type.UNORDERED_LIST, scope, [tokens[0]])
            return self.__open_recursively(tokens[2:]) + 2
               
        if len(tokens) > 3 and tokens[0].kind is Token.Type.NUMBER and tokens[1].kind is Token.Type.PERIOD and tokens[2].kind is Token.Type.SPACE:
            self.__open_structure(Structure.Type.ORDERED_LIST, scope, [tokens[0]])
            return self.__open_recursively(tokens[3:]) + 3

        # To enable lists embedded in other lists, the inner lists are padded by a space
        if len(tokens) > 2 and (tokens[0].kind in [Token.Type.DASH, Token.Type.PLUS] or tokens[0].value == "*") and tokens[1].kind is Token.Type.SPACE:
            self.__open_structure(Structure.Type.UNORDERED_LIST, scope, [tokens[0]])
            return self.__open_recursively(tokens[2:]) + 2
               
        if len(tokens) > 3 and tokens[0].kind is Token.Type.NUMBER and tokens[1].kind is Token.Type.PERIOD and tokens[2].kind is Token.Type.SPACE:
            self.__open_structure(Structure.Type.ORDERED_LIST, scope, [tokens[0]])
            return self.__open_recursively(tokens[3:]) + 3

        if len(tokens) > 2 and tokens[0].kind is Token.Type.HASH and tokens[1].kind is Token.Type.SPACE:
            self.__open_structure(Structure.Type[f"HEADING_{len(tokens[0].value)}"], scope, [tokens[0]])
            return 2
                    
        if scope is None:
            self.__open_structure(Structure.Type.PARAGRAPH, scope)
        return 0

    def __finish_current_structure(self):
        """
        Removes the structure on the top of the context stack and adds it to the content of its parent structure. If the token buffer is not empty,
        it is concatenated as TEXT structure, which is appended to the structure on the top's content (not the parent's).
        """
        # This should not happen, but it still prevents the crash :0
        if self.context_stack.get_last().kind is Structure.Type.SUPER:
            return
        # Finishing a structure usually means changing scope, so we need to reset the metadata gathered for links
        if self.context_stack.get_last().kind not in [Structure.Type.TEXT, Structure.Type.LINK] and self.link_buffer_stage != 1:
            self.__reset_link_metadata()
        if len(self.token_buffer) > 0:
            # If the structure already is TEXT, we simply append the buffer to the text in the structure
            if self.context_stack.get_last().kind is Structure.Type.TEXT:
                self.context_stack.get_last().content += self.__stringify_tokens(self.token_buffer)
            else:
                text_structure = Structure(self.__stringify_tokens(self.token_buffer), Structure.Type.TEXT, self.__get_current_scope())
                self.context_stack.get_last().content.append(text_structure)
            self.__clear_buffer()
        self.context_stack.get_last().parent.content.append(self.context_stack.poll())
        
    def __finish_structure(self, kind):
        """
        Closes all currently open structures on the context stack until a structure of the type of @kind is found. MAKE SURE SUCH A STRUCTURE EXISTS, otherwise it will wipe the context stack and
        raise an ERROR!
        """
        while (structure := self.context_stack.get_last()).kind is not kind:
            self.__finish_current_structure()
        self.__finish_current_structure()

    def __finish_recursively(self, scopes):
        """
        Closes all structures on the context stack that belong to the scopes in the @scopes list. The scopes are closed in the same order as they are in the list.
        Empties the @scopes list.
        """
        if len(scopes) == 0:
            return
        scope = scopes[0]
        structure = self.context_stack.get_last()
        while structure.scope is scope:
            if self.__finish_recursively__is_false_positive(structure, scope):
                break
            self.__finish_current_structure()
            structure = self.context_stack.get_last()
        # The scope-opening structure actually does not itself belong to the scope (unless false-positive) so we need to close one more structure to the top
        self.__finish_current_structure()
        scopes.pop(0)
        self.__finish_recursively(scopes)
        
    def __finish_recursively__is_false_positive(self, structure, scope):
        """
        Checks whether a structure is a false positive for a scope check. 
        
        The scope of a structure is determined by its parent. That means that by default, a BLOCKQUOTE
        structure may not have any scope if it is on level zero, but its children will have the scope BLOCKQUOTE. To close a BLOCKQUOTE then, you simply close all the
        structures with the scope BLOCKQUOTE (and the BLOCKQUOTE itself). However if a BLOCKQUOTE structure is nested inside another BLOCKQUOTE structure, it will also have the scope BLOCKQUOTE as
        it is a child of a BLOCKQUOTE structure. Therefore it is a false positive.
        
        Returns boolean.
        """
        match scope:
            case Structure.Scope.BLOCKQUOTE:
                return structure.kind is Structure.Type.BLOCKQUOTE
            case Structure.Scope.PARAGRAPH:
                return structure.kind is Structure.Type.PARAGRAPH
            case Structure.Scope.LIST:
                return structure.kind is Structure.Type.ORDERED_LIST or structure.kind is Structure.Type.UNORDERED_LIST
        return False
    
    def __get_current_scope(self):
        """
        Determines the scope for the next-to-be-opened structure. This scope may differ from the scope of its parent structure.
        Returns {@link Structure.Type}.
        """
        match self.context_stack.get_last().kind:
            case Structure.Type.BLOCKQUOTE:
                return Structure.Scope.BLOCKQUOTE
            case Structure.Type.CODEBLOCK:
                return Structure.Scope.CODEBLOCK
            case Structure.Type.CODE:
                return Structure.Scope.CODE
            case Structure.Type.HTML:
                return Structure.Scope.HTML
            case Structure.Type.PARAGRAPH:
                return Structure.Scope.PARAGRAPH
            case Structure.Type.ORDERED_LIST:
                return Structure.Scope.LIST
            case Structure.Type.UNORDERED_LIST:
                return Structure.Scope.LIST
            case _:
                if str(self.context_stack.get_last().kind).startswith("HEADING"):
                    return Structure.Scope.HEADING
                return self.context_stack.get_last().scope
    
    def __get_scope_hierarchy(self):
        """
        Traverses the context stack and generates a list of the open scopes from bottom to the top.
        Returns a list.
        """
        scope_structures = [Structure.Type.BLOCKQUOTE, Structure.Type.CODEBLOCK, Structure.Type.CODE, Structure.Type.PARAGRAPH, Structure.Type.ORDERED_LIST,
            Structure.Type.UNORDERED_LIST]
        scopes = []
        structure = self.context_stack.get_last()
        # Add current scope only if it is not inherited (avoid adding the same scope twice)
        if (current := self.__get_current_scope()) is not None and  self.__finish_recursively__is_false_positive(structure, current):
            scopes.append(current)
        
        while structure is not None:
            if structure.scope is None:
                break
            if structure.parent is None:
                break
            if structure.parent.kind in scope_structures or str(structure.parent.kind).startswith("HEADING"):
                scopes.append(structure.scope)
            structure = structure.parent
        return list(reversed(scopes))

    def __get_open_structure(self, kind):
        """
        Finds the last open structure of the type @kind on the context stack.
        Returns
                a) a {@link Structure}
                b) None if no such structure is open.
        """
        structure = self.context_stack.get_last()
        while structure is not None:
            if structure.kind is kind:
                return structure
            if structure.parent is None:
                break
            structure = structure.parent
        return None

    def __rstrip_tokens(self, tokens):
        """
        Removes all trailing SPACE tokens from @tokens. The modifications are done directly to the list. Returns the length difference between the original and the
        modified list.
        Returns an integer.
        """
        diff = 0
        while len(tokens) > 1 and tokens[-1].kind is Token.Type.SPACE:
            diff += len(tokens[-1].value)
            tokens.pop()
        return diff
            
    def __shift_by_scope(self, tokens, scope, HAS_NESTED_LISTS=False):
        """
        Removes the appropriate opening tokens for the given @scope from @tokens. Only block-level scopes are removed. The list @tokens is not altered.
        Returns
                a) a list of tokens without the scope prefix
                b) False if the shift failed
        """
        match scope:
            case Structure.Scope.BLOCKQUOTE:
                if len(tokens) > 2 and tokens[0].kind is Token.Type.GT and tokens[1].kind is Token.Type.SPACE:
                    return tokens[2:]
                # Enable lazy BLOCKQUOTE markup
                if not self.__is_line_empty(tokens):
                    return tokens
            case Structure.Scope.CODEBLOCK:
                if len(tokens) >= 2:
                    if tokens[0].kind is Token.Type.SPACE and len(tokens[0].value) >= 4:
                        if len(tokens[0].value) == 4:
                            return tokens[1:]
                        else:
                            tokens[0].value = tokens[0].value[4:]
                            return tokens
            case Structure.Scope.LIST:
                if len(tokens) > 2 and (tokens[0].kind in [Token.Type.DASH, Token.Type.PLUS] or tokens[0].value == "*") and tokens[1].kind is Token.Type.SPACE:
                    if HAS_NESTED_LISTS is True:
                        return False
                    self.__finish_structure(Structure.Type.LIST_ITEM)
                    self.__open_structure(Structure.Type.LIST_ITEM)
                    return tokens[2:] # Unoredered list
                
                if len(tokens) > 3 and tokens[0].kind is Token.Type.NUMBER and tokens[1].kind is Token.Type.PERIOD and tokens[2].kind is Token.Type.SPACE:
                    if HAS_NESTED_LISTS is True:
                        return False
                    self.__finish_structure(Structure.Type.LIST_ITEM)
                    self.__open_structure(Structure.Type.LIST_ITEM)
                    return tokens[3:] # Ordered list
                # Enable multi-line list items
                if not self.__is_line_empty(tokens):
                    # We all a double-space prefix to qualify as continuation of the LIST_ITEM to allow lists inside list items
                    if len(tokens) >= 2 and tokens[0].kind is Token.Type.SPACE and len(tokens[0].value) >= 2:
                        if len(tokens[0].value) == 2:
                            return tokens[1:]
                        else:
                            tokens[0].value = tokens[0].value[2:]
                            return tokens
                    else:
                        return tokens # If the line is just regular paragraph of text or something, we let it pass
               # empty = self.__is_line_empty(tokens)
               # if self.FLAG_LAST_LINE_EMPTY is True and len(tokens) > 2 and tokens[0].kind is Token.Type.SPACE and not empty:
                   # self.__wrap_top_text_in_paragraph()
                    #return tokens[1:]
                #elif not empty:
                    #self.__wrap_top_text_in_paragraph()
                    #return tokens # Allow multiline list items
            case Structure.Scope.CODE:
                return tokens # CODE is not a block level scope
            case Structure.Scope.PARAGRAPH:
                return tokens # PARAGRAPH has no special opening
        return False
    
    def __stringify_tokens(self, tokens):
        """
        Converts a list of tokens to its string representation. Line breaks are introduced back into the string. 
        Tabs are converted to spaces. Other than that it is a reverse process to tokenization. The string contains the text of the tokens in the
        order the tokens were added to the list. The line positions of the tokens are not given any notice, same for line numbers.
        Returns a string.
        """
        string = ""
        for token in tokens:
            match token.kind:
                case Token.Type.TEXT:
                    string += token.value
                case Token.Type.SPACE:
                    string += token.value
                case Token.Type.TAB:
                    string += " " * 4
                case Token.Type.EOL:
                    string += "\n"
                case Token.Type.BACKSLASH:
                    string += "\\"
                case Token.Type.HASH:
                    string += token.value
                case Token.Type.GT:
                    string += ">"
                case Token.Type.LT:
                    string += "<"
                case Token.Type.NUMBER:
                    string += token.value
                case Token.Type.EXCLAMATION_MARK:
                    string += "!"
                case Token.Type.DASH:
                    string += "-"
                case Token.Type.ASTERISK:
                    string += token.value
                case Token.Type.UNDERSCORE:
                    string += token.value
                case Token.Type.PLUS:
                    string += "+"
                case Token.Type.TILDE:
                    string += "~"
                case Token.Type.EQUALS:
                    string += "="
                case Token.Type.LPAREN:
                    string += "("
                case Token.Type.RPAREN:
                    string += ")"
                case Token.Type.LBRACKET:
                    string += "["
                case Token.Type.RBRACKET:
                    string += "]"
                case Token.Type.LBRACE:
                    string += "{"
                case Token.Type.RBRACE:
                    string += "}"
                case Token.Type.DOUBLE_QUOTES:
                    string += "\""
                case Token.Type.SINGLE_QUOTES:
                    string += "'"
                case Token.Type.COLON:
                    string += ":"
                case Token.Type.BACKTICK:
                    string += token.value
                case Token.Type.PERIOD:
                    string += "."
                case Token.Type.SEMICOLON:
                    string += ";"
        return string
    
    
