"""
Basic calculator script that accepts an arithmetic expression such as (3 + 2)*8 and returns the result. If you simply use `eval()`, I suppose it will be more efficient.

A good improvement would be to add support for functions like exponentiation, square root, logarithm, etc. Maybe add floating point division and modulus?
Let user define variables and constants?
"""

DEBUG = False
        
OPERATORS = {
    "+": (lambda a, b: a + b),
    "-": (lambda a, b: a - b),
    "*": (lambda a, b: a * b),
    "/": (lambda a, b: a // b)
}

def convert_to_postfix(expr):
    """
    Converts the string @expr which is expected to contain an arithmetic expression in the infix notation to a string in the postfix notation.
    Returns string.
    """
    output = ""
    stack = list()
    for token in expr.split(" "):
        if token.isdecimal():
            output += token + " "
        elif token == '(':
            stack.append(token)
        elif token == ')':
            while len(stack) != 0:
                if stack[-1] == '(':
                    stack.pop()
                    break
                output += stack.pop() + " "
        elif token in ['+', '-', '*', '/']:
            while len(stack) != 0:
                if stack[-1] == '(':
                    break
                l = stack[-1]
                if token in ['*', '/'] and l in ['+', '-']:
                    break
                output += l + " "
                stack.pop()
            stack.append(token)
    output = (output + " ".join(reversed(stack))).rstrip()
    if DEBUG == True:
        print(f"postfix: {output}")
    return output

def evaluate_postfix(expr):
    """
    Takes a string @expr that contains an arithmetic expression in postfix notation and calculates its numeric value.
    Returns integer.
    """
    stack = list()
    data = expr.split(" ")
    for token in data:
        if token.isdecimal():
            stack.append(int(token))
        elif token in ['+', '-', '*', '/']:
            b = stack.pop()
            a = stack.pop()
            stack.append(OPERATORS[token](a, b))
    if DEBUG == True:
        print(f"postfix value: {stack[-1]}")
    return stack.pop()
    
def add_spaces(expr):
    """
    Takes a string @expr in infix notation and supplements it with additional spaces to make the expression valid. This is for user convenience as they can now write
            (3+5)*7 
    instead of
            ( 3 + 5 ) * 7.
    Returns string.
    """
    output = ""
    for i in range(len(expr) - 1):
        token = expr[i]
        output += token
        if token in ['(', ')', '+', '-', '*', '/'] and expr[i+1] != ' ':
            output += ' '
        elif token.isdecimal() and not (expr[i+1].isdecimal() or expr[i+1] == ' '):
            output += ' '
    output += expr[-1]
    output = output.strip()
    if DEBUG == True:
        print(f"spaced to: {output}")
    return output
    
def evaluate(expr):
    if DEBUG == True:
        print(f"input: {expr}")
    formatted = add_spaces(expr)
    postfix = convert_to_postfix(formatted)
    return evaluate_postfix(postfix)

########################################### TEST AREA ################################

def test__convert_to_postfix():
    test_inputs = ["( 2 + 5 ) * ( 13 - 4 )", "( ( 3 + 5 ) * 1 ) + 2"]
    test_results = ["2 5 + 13 4 - *", "3 5 + 1 * 2 +"]
    for i in range(len(test_inputs)):
        result = convert_to_postfix(test_inputs[i])
        assert result == test_results[i], f"test {i+1} failed: {result} expected: {test_results[i]}"

def test__evaluate_postfix():
    test_inputs = ["2 5 + 13 4 - *", "3 5 + 1 * 2 +"]
    test_results = [63, 10]
    for i in range(len(test_inputs)):
        result = evaluate_postfix(test_inputs[i])
        assert result == test_results[i], f"test {i+1} failed: {result} expected: {test_results[i]}"
        
def test__add_spaces():
    test_inputs = ["(2 + 5)*(13 - 4)", "((3 + 5)*1) + 2"]
    test_results = ["( 2 + 5 ) * ( 13 - 4 )", "( ( 3 + 5 ) * 1 ) + 2"]
    for i in range(len(test_inputs)):
        result = add_spaces(test_inputs[i])
        assert result == test_results[i], f"test {i+1} failed: {result} expected: {test_results[i]}"

def test__evaluate():
    test_inputs = ["12*(3+(8-2)+1)", "63/3*6", "15-8*4-30/(2+8)"]
    test_results = [120, 126, -20]
    for i in range(len(test_inputs)):
        result = evaluate(test_inputs[i])
        assert result == test_results[i], f"test {i+1} failed: {result} expected: {test_results[i]}"

def test():
    test__convert_to_postfix()
    test__evaluate_postfix()
    test__add_spaces()
    test__evaluate()

#######################################################################################


def main():
    fail = '\033[91m'
    end = '\033[0m'
    print("Type 'exit' to close the program.")
    while (expr := input("Enter expression: ").strip()) not in ["exit", "quit", "close"]:
        if expr.endswith("-d"):
            expr = expr[:-2]
            global DEBUG
            DEBUG = not DEBUG
        try:
            result = evaluate(expr)
            print(f"> {result}")
        except ZeroDivisionError:
            print(f"{fail}zero division{end}")
        except:
            print(f"{fail}invalid expression format{end}")
        
test()

if __name__ == "__main__":
    main()
