#Name : KWOK Hoi Yi, Any ID: 22000531
#159.341 Assignment 1 - A parser/interpreter for a simple, imperative string-processing language

import re

# ======  ERRORS  ========
def InvalidExactSizeError(expectedSize, command_type):
  print(f'Invalid Syntax: Expected EXACTLY {expectedSize} tokens in {command_type} statement')

def InvalidSizeError(expectedSize, command_type):
  print(f'Invalid Syntax: Expected MORE THAN {expectedSize} tokens in {command_type} statement')

def InvalidSyntaxError(expectedToken, expectedPosition):
  print(f'Invalid Syntax: Expected {expectedToken} {expectedPosition}')

def InvalidTokenError(currentTokenType, expectedTokenType, state):
  print(f'Invalid Token: {currentTokenType} - Expected {expectedTokenType} for {state}')

def InvalidCharError(char):
  print(f'Invalid Char: "{char}" - Only ";", "+", command or id(start with letter) for Non-Literal Token')

def RunTimeError(details):
  print(f'Runtime Error: {details}')

# ======  LEXER LAYER  ========
## TOKEN

# Regular Expression foe each token type
token_regex = {
    "command": r"\b(append|exit|list|print|printlength|printwords|printwordcount|set|reverse)\b",
    "constant": r"SPACE|TAB|NEWLINE",
    "end": r";",
    "plus": r"\+",
    "id": r"[a-zA-Z][a-zA-Z0-9]*",
    "literal": r'"(?:\\.|[^"\\]|(?:\\\n))*"'
}

regexs = {token: re.compile(regex) for token, regex in token_regex.items()}

class Token:
    def __init__(self, type_, value=None):
        self.type = type_
        self.value = value

def lexer(text):

    tokens = []
    index = 0

    while index < len(text):

        if text[index] == '"':
            end_quote_index = index + 1
            while True:
                if '\n' in text[index:end_quote_index]:
                    index = text.find('\n', end_quote_index) + 1
                    end_quote_index = index
                    continue

                end_quote_index = text.find('"', end_quote_index)  # Find the next '"'s index
                if end_quote_index == -1:  # No " in the token
                    InvalidSyntaxError('"', 'at the end of literal token')
                    return
                elif text[end_quote_index - 1] != '\\':  # Check if it's an escaped "
                    break
                else:
                    end_quote_index += 1

            value = text[index:end_quote_index + 1]
            tokens.append(Token("literal", value))
            index = end_quote_index + 1

        elif text[index] in (' ', '\n', '\t'):  # skip whitespace
            index += 1
        elif text[index].isalpha() or text[index] in (';', '+'):
            for token_type, pattern in regexs.items():
                match = pattern.match(text, index)
                if match:
                    value = match.group()
                    tokens.append(Token(token_type, value))
                    index = match.end()
                    break
        else:
            InvalidCharError(text[index])
            return

    return tokens


# ======  PARSER LAYER  ========

def all_variables_defined(statement):
    for i, token in enumerate(statement):
        if token.type == 'id' and token.value not in variables:
            RunTimeError(f"Variable '{token.value}' not defined")
            return False
    return True

def is_exact_length(statement, expected_length, command_type):
    if len(statement) != expected_length:
        InvalidExactSizeError(expected_length, command_type)
        return False
    return True

def is_correct_length(statement, expected_length, command_type):
    if len(statement) < expected_length:
        InvalidSizeError(expected_length, command_type)
        return False
    return True

def parse_value_(values):
    value = ''
    for sublist in values:
        for token in sublist:
            if token.type == 'id':
                value += variables[token.value]

            elif token.type == 'constant':
                if token.value == 'SPACE':
                    value += ' '
                elif token.value == 'TAB':
                    value += '\t'
                elif token.value == 'NEWLINE':
                    value += '\n'

            elif token.type == 'literal':
                literal_value = token.value[1:-1]  # skip ""
                literal_value = literal_value.replace(r'\\', '\\')  # \\ -> \
                literal_value = literal_value.replace(r'\"', '"')  # \" -> "
                value += literal_value
    return value

def parse_expression(expression_tokens):
    error = False
    values = []  # values is a list of token
    while expression_tokens:
        for i, token in enumerate(expression_tokens):
            if error:  break # if error,  break
            if token.type == 'command':
                InvalidTokenError('command', 'value (id | constant | literal)','expression')
                error = True
                return

            if token.type == 'plus': # split expression to value by +(if any)
                end_index = i
                value = expression_tokens[:end_index]
                values.append(value)
                expression_tokens = expression_tokens[end_index + 1:]
                break
        else: # last value
            values.append(expression_tokens)
            break
    return parse_value_(values)

def parse_statement(statements):  ## check grammar
    for statement in statements:
        if statement[-1].type == 'end':  # Check if the statement ends with 'END' token
            if statement[0].type == 'command':  # Check if the first token is a command
                if statement[0].value == 'append':
                    parse_append_statement(statement)
                elif statement[0].value == 'list':
                    parse_list_statement(statement)
                elif statement[0].value == 'exit':
                    parse_exit_statement(statement)
                elif statement[0].value == 'print':
                    parse_print_statement(statement)
                elif statement[0].value == 'printlength':
                    parse_printlength_statement(statement)
                elif statement[0].value == 'printwords':
                    parse_printwords_statement(statement)
                elif statement[0].value == 'printwordcount':
                    parse_printwordcount_statement(statement)
                elif statement[0].value == 'set':
                    parse_set_statement(statement)
                elif statement[0].value == 'reverse':
                    parse_reverse_statement(statement)
            else:
                InvalidSyntaxError("COMMAND", "at the beginning of statement")
        else:
            InvalidSyntaxError(";", "at the end of statement")

def parse_program(tokens):
    statements = []  # Program is a list of statements
    while tokens:
        for i, token in enumerate(tokens):
            if token.type == 'end': # split input to statements by ;
                end_index = i
                statement = tokens[:end_index + 1]
                statements.append(statement)
                tokens = tokens[end_index + 1:]
                break
        else:
            # put the remaining tokens as the last statement
            statements.append(tokens)
            break
    return statements

def parse_append_statement(statement):
    if not is_correct_length(statement, 4, 'APPEND'): return
    statement.pop(0)  ## skip command
    if not all_variables_defined(statement): return

    second_token = statement.pop(0)
    variable_name = second_token.value
    expression_value = parse_expression(statement)

    variables[variable_name] += expression_value

def parse_list_statement(statement):
    if not is_exact_length(statement, 2, 'LIST'): return
    elif variables:
        print(f'Identifier List ({len(variables)}): ')
        for variable, value in variables.items():
            print(f"{variable}: {value}")
    else: RunTimeError("No Variable in the list")

def parse_exit_statement(statement):
    if not is_exact_length(statement, 2, 'EXIT'): return
    else: exit(0)

def parse_print_statement(statement):
    if not is_correct_length(statement, 3, 'PRINT'): return
    if not all_variables_defined(statement): return

    statement.pop(0)  ## skip command
    expression_value = parse_expression(statement)
    print(expression_value)

def parse_printlength_statement(statement):
    if not is_correct_length(statement, 3, 'PRINTLENGTH'): return
    if not all_variables_defined(statement): return

    statement.pop(0)  ## skip command
    expression_value = parse_expression(statement)
    print("Length is:", len(expression_value))

def parse_printwords_statement(statement):
    if not is_correct_length(statement, 3, 'PRINTWORDS'): return
    if not all_variables_defined(statement): return

    statement.pop(0)  ## skip command
    expression_value = parse_expression(statement)

    words = re.findall(r'\b[\w\'-]+\b', expression_value)
    print("Words are:")
    for word in words:
        print(word)

def parse_printwordcount_statement(statement):
    if not is_correct_length(statement, 3, 'PRINTWORDCOUNT'): return
    if not all_variables_defined(statement): return

    statement.pop(0)  # skip command
    expression_value = parse_expression(statement)
    words = re.findall(r'\b[\w\'-]+\b', expression_value)
    words = [word for word in words if any(char.isalnum() for char in word)]
    print("Word count is:", len(words))

def parse_set_statement(statement):
    if not is_correct_length(statement, 4, 'SET'): return
    statement.pop(0)  ## skip command

    second_token = statement.pop(0)
    if second_token.type != 'id':
        InvalidTokenError(second_token.type, "id", "Set")
        return

    if not all_variables_defined(statement): return
    expression_value = parse_expression(statement)
    variables[second_token.value] = expression_value

def parse_reverse_statement(statement):
    if not is_exact_length(statement, 3, 'REVERSE'): return

    statement.pop(0)  ## skip command

    second_token = statement.pop(0)
    if second_token.type != 'id':
        InvalidTokenError(second_token.type, "id", "reverse")
        return
    if second_token.value not in variables:
        RunTimeError(f"Variable '{second_token.value}' not defined")
        return

    words = variables[second_token.value].split()
    variables[second_token.value] = ' '.join(words[::-1])

if __name__ == "__main__":
    variables = {}
    print("----------------------------------------")
    print(" 159.341 Assignment 1 Semester 1 2024 ")
    print(" Submitted by: Any KWOK, 22000531 ")
    print("----------------------------------------")

    while True:
        text = input("＿ﾉ乙(ཀﾝ､)ノ >> ")
        tokens = lexer(text)
        statements = parse_program(tokens)
        if statements:
            parse_statement(statements)