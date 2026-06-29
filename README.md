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
* User-defined functions (`defun`)
* Lexical scoping
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

>>> (defun square (n) (* n n))

>>> (square 5)
25
```

## Usage

### REPL

Start the REPL:

```bash
python hith.py
```

### Use from Code

```python
from evaluate import Evaluator

evaluator = Evaluator()

print(evaluator.evaluate("(+ 1 2)"))
```

Output:

```lisp
3
```

## Language Overview

### Values

```lisp
>>> 42
42

>>> 3.14159
3.14159

>>> "Hello, world!"
"Hello, world!"
```

### Arithmetic

```lisp
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
```

### Variables

```lisp
>>> (defvar x 10)
x

>>> (defvar y 20)
y

>>> x
10

>>> (symbol-value 'x)
10

>>> (setq z 40)
z

>>> (symbol-value 'z)
40
```

### Comparisons

```lisp
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

### Conditionals

```lisp
>>> (if True 1 2)
1

>>> (if False 1 2)
2

>>> (if (< x y) (+ x y) (- x y))
30
```

### User-defined Functions

```lisp
>>> (defun square (n) (* n n))
square

>>> (square 5)
25

>>> (defun add (a b) (+ a b))
add

>>> (add 3 4)
7

>>> (defvar x 100)
x

>>> (square x)
10000
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
| `defun` | Define a user-defined function |

## User-defined Functions

Functions are defined with `defun`.

```lisp
(defun square (n)
  (* n n))

(square 9)
```

Result:

```lisp
81
```

Functions may take multiple parameters.

```lisp
(defun max2 (a b)
  (if (> a b)
      a
      b))

(max2 10 4)
```

Result:

```lisp
10
```

Functions execute in their own lexical environment. Parameter bindings
are local to the function while global variables and functions remain
accessible through the parent environment.

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

Recursively evaluates the AST. Special forms (`if`, `setq`, `defvar`,
and `defun`) receive their arguments unevaluated, while normal
functions evaluate all arguments before invocation.

Evaluation happens within an `Env` object, allowing environments to be
nested through parent environments. User-defined functions create a
new environment whose parent is the environment in which the function
was defined, providing lexical scope.

## Running Tests

Run all tests:

```bash
python -m unittest discover
```

Or run individual test files:

```bash
python test_lexer.py
```

## Current Limitations

* Function bodies currently consist of a single expression
* No lists
* Limited error handlingg