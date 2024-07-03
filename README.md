# Simple Imperative String-Processing Language Interpreter

## Overview

This project is an interpreter for a simple imperative string-processing language, developed as part of the 159.341 course assignment at Massey University. The interpreter processes and executes commands related to string manipulation.

## Author

- **Name:** KWOK Hoi Yi
- **Student ID:** 22000531

## Course Details

- **Course:** 159.341
- **Assignment:** 1
- **Semester:** 1, 2024

## Features

This interpreter supports the following commands:
- `append`: Appends a string to a variable.
- `exit`: Terminates the interpreter.
- `list`: Lists all defined variables and their values.
- `print`: Prints a string.
- `printlength`: Prints the length of a string.
- `printwords`: Prints all words in a string.
- `printwordcount`: Prints the number of words in a string.
- `set`: Sets a variable to a specified string.
- `reverse`: Reverses the words in a string.

## Usage

1. Run the interpreter.
2. Enter commands at the prompt `＿ﾉ乙(ཀﾝ､)ノ >> `.
3. The interpreter will process the commands and display the results.

## Error Handling

The interpreter includes robust error handling for various syntax and runtime errors:
- Invalid command syntax
- Undefined variables
- Invalid tokens and characters
- Runtime errors during execution

## Code Structure

- **Lexer Layer:** Tokenizes the input commands using regular expressions.
- **Parser Layer:** Parses the tokens into statements and executes the appropriate command functions.
- **Error Handling:** Provides specific error messages for different types of errors.

## Example

```Sample
＿ﾉ乙(ཀﾝ､)ノ >> set myVar "Hello, World!";
＿ﾉ乙(ཀﾝ､)ノ >> print myVar;
Hello, World!
＿ﾉ乙(ཀﾝ､)ノ >> append myVar " How are you?";
＿ﾉ乙(ཀﾝ､)ノ >> print myVar;
Hello, World! How are you?
＿ﾉ乙(ཀﾝ､)ノ >> printlength myVar;
Length is: 24
＿ﾉ乙(ཀﾝ､)ノ >> printwords myVar;
Words are:
Hello
World
How
are
you
＿ﾉ乙(ཀﾝ､)ノ >> printwordcount myVar;
Word count is: 5
＿ﾉ乙(ཀﾝ､)ノ >> reverse myVar;
＿ﾉ乙(ཀﾝ､)ノ >> print myVar;
you? are How World! Hello,
＿ﾉ乙(ཀﾝ､)ノ >> exit;
```

## Dependencies

- Python 3.x
- `re` module (part of the Python Standard Library)

## Running the Code

To run the interpreter, execute the following command in your terminal:

```sh
python interpreter.py
```

## Contact

For any questions or issues, please contact Any KWOK at [yiamy1202@yahoo.com.hk].
