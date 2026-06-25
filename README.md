# Hith

A Lisp interpreter written in Python.

Hith supports:

* Arithmetic operations
* Comparison operators
* Boolean values (`True` and `False`)
* Variables
* Symbol lookup
* Integers and floating point numbers
* Strings
* Nested expressions
* S-expression syntax

## Why the name Hith?

It sounds like a snake hissing with a lisp. :)
 
## Example

```lisp
>>> (defvar x 10)
>>> (defvar y 20)

>>> (* x 3)
30

>>> (< x y)
True

>>> (eq x y)
False
```

## Usage

### Repl

Start the REPL:

```bash
python hith.py
```

### Use from Code

```python
from evaluate import evaluate

print(evaluate("(+ 1 2)"))
```

Output:

```lisp
3
```

## Language Overview

```lisp
>>> 42
42

>>> 3.14159
3.14159

>>> "Hello, world!"
"Hello, world!"

>>> (+ 1 2)
3

>>> (- 10 3)
7

>>> (* 4 5)
20

>>> (/ 20 4)
5

>>> (+ 1 (+ 2 3))
6

>>> (defvar x 10)
10

>>> (defvar y 20)
20

>>> x
10

>>> (symbol-value 'x)
10

>>> (> y x)
True

>>> (< x y)
True

>>> (>= x 10)
True

>>> (<= x 5)
False

>>> (eq x y)
False

>>> (eq (< x y) (> y x))
True
```

## Built-in Functions

| Function | Description |
|----------|-------------|
| `+` | Addition |
| `-` | Subtraction |
| `*` | Multiplication |
| `/` | Division |
| `>` | Greater than |
| `<` | Less than |
| `>=` | Greater than or equal |
| `<=` | Less than or equal |
| `eq` | Equality comparison |
| `defvar` | Define a variable |
| `symbol-value` | Return a variable's value |

## Architecture

The interpreter consists of three stages.

### Lexer

Converts source code into tokens.

Input:

```lisp
>>> (+ 1 2)
```

Output:

```python
['(', '+', '1', '2', ')']
```

### Parser

Converts tokens into an Abstract Syntax Tree (AST).

Output:

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

* No conditionals (`if`)
* No user-defined functions
* No lists
* No lexical scope
* Limited error handling