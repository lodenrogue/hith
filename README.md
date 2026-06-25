# Hiss

A Lisp interpreter written in Python.

Hiss supports:

* Arithmetic operations
* Nested expressions
* Variables
* Symbol lookup
* Integers and floating point numbers
* Strings
* S-expression syntax

## Example

```lisp
(+ 1 2)
=> 3

(* 3 (+ 4 (- 13 6)))
=> 33
```

## Usage

### Repl

To start the repl you can run:

```bash
python hiss.py
```

### Use from code

To use hiss from Python code you can do:

```python
from evaluate import evaluate

print(evaluate("(+ 1 2)"))
```

Output:

```text
3
```

## Language Overview

### Numbers and Strings

```lisp
42

3.14159

"Hello, world!"

"hello() 33.23 world"
```

### Arithmetic

```lisp
(+ 1 2)
=> 3

(- 10 3)
=> 7

(* 4 5)
=> 20

(/ 20 4)
=> 5

(+ 1 (+ 2 3))
=> 6

(* (* 3 4) 6)
=> 72
```

### Variables

```lisp
(defvar x 10)

x
=> 10

(symbol-value 'x)
=> 10
```

## Built-in Functions

| Function       | Description               |
| -------------- | ------------------------- |
| `+`            | Addition                  |
| `-`            | Subtraction               |
| `*`            | Multiplication            |
| `/`            | Division                  |
| `defvar`       | Define a variable         |
| `symbol-value` | Return a variable's value |

## Example Session

```lisp
(defvar price 15)
(defvar quantity 3)

(* price quantity)
=> 45

(defvar greeting "Hello, world!")

(symbol-value 'greeting)
=> "Hello, world!"

(* 3 (+ 4 (- 13 6)))
=> 33
```

## Architecture

The interpreter consists of three stages.

### Lexer

Converts source code into tokens.

Example:

```lisp
(+ 1 2)
```

Produces:

```python
['(', '+', '1', '2', ')']
```

### Parser

Converts tokens into an Abstract Syntax Tree (AST).

Example:

```python
["+", 1, 2]
```

### Evaluator

Recursively evaluates the AST and executes functions.

## Running Tests

Run all tests:

```bash
python -m unittest discover
```

Or run individual test files:

```bash
python test_lexer.py
python test_parser.py
python test_math.py
python test_variables.py
```

## Current Limitations

* No booleans
* No conditionals (`if`)
* No comparison operators (`>`, `<`, `=`, etc.)
* No user-defined functions
* No lists
* No quoting
* No lexical scope
* No error handling for malformed programs