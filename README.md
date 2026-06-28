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
* Conditionals (`if`)
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

>>> (if (< x y) "smaller" "larger")
"smaller"

>>> (eq x y)
False
```

## Usage

### REPL

Start the REPL:

```bash
python hith.py
```

### Use from Code

```python
from evaluate import Evaluator, Env, Variables

variables = Variables()
env = Env(variables=variables, parent=None)
evaluator = Evaluator(env)

print(evaluator.evaluate("(+ 1 2)"))
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
5.0

>>> (+ 1 (+ 2 3))
6

>>> (defvar x 10)
x

>>> (defvar y 20)
y

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

>>> (if True 1 2)
1

>>> (if False 1 2)
2

>>> (if (< x y) (+ x y) (- x y))
30

>>> (setq z 40)
z

>>> (symbol-value 'z)
40

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
| `if` | Conditional expression (special form) |
| `defvar` | Define a variable in the current environment |
| `setq` | Define a variable in the current environment |
| `symbol-value` | Return the value of a symbol |

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

Recursively evaluates the AST. Special forms (`if`, `setq`, and
`defvar`) receive their arguments unevaluated, while normal functions
evaluate all arguments before invocation.

Evaluation happens within an `Env` object, allowing environments to be
nested through parent environments.

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

* No user-defined functions
* No lists
* No lexical scope
* Limited error handling