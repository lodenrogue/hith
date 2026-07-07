# Hith

A Lisp interpreter, written from scratch in Python. Hith has s-expression syntax, lexical scoping with closures, macros with quasiquotation, and a small standard library of loops and helpers written in Hith itself.

Hith supports:

- Arithmetic and comparison operators
- `t` / `nil` as true and false
- Variables (`defvar`, `setq`) and symbol lookup
- Integers and floats (mixing the two promotes to float)
- Strings
- Lists, and list operations (`list`, `cons`, `car`, `cdr`, `nth`, `length`)
- Conditionals (`if`, `cond`)
- Loops (`while`, `for`, `range`, `foreach`)
- User-defined functions (`defun`) with multi-expression bodies
- Lexical scoping and closures
- Macros (`defmacro`) with backquote/unquote/unquote-splice
- Type predicates (`atom`, `intp`, `floatp`, `stringp`, `symbolp`)
- Randomness (`random`, `randrange`, `choice`)
- Reading files (`file-read-lines`)
- Printing to standard out (`message`, `format`)
- Running scripts, with command-line arguments passed through

## Contents

- [Why the name Hith?](#why-the-name-hith)
- [Quick Example](#quick-example)
- [Requirements](#requirements)
- [Usage](#usage)
  - [REPL](#repl)
  - [Run a Hith Script](#run-a-hith-script)
  - [Use Hith from Python Code](#use-hith-from-python-code)
- [Language Overview](#language-overview)
  - [Values](#values)
  - [Arithmetic](#arithmetic)
  - [Variables](#variables)
  - [Printing](#printing)
  - [Comparisons](#comparisons)
  - [Conditionals](#conditionals)
  - [Loops](#loops)
  - [Lists](#lists)
  - [Functions](#functions)
  - [Macros](#macros)
  - [Symbols](#symbols)
  - [Type Predicates](#type-predicates)
  - [Randomness](#randomness)
  - [Files](#files)
  - [Sequencing with progn](#sequencing-with-progn)
  - [Miscellaneous](#miscellaneous)
- [Quick Reference](#quick-reference)
- [Architecture](#architecture)
- [Running Tests](#running-tests)
- [Current Limitations](#current-limitations)

## Why the name Hith?

It sounds like a snake hissing with a lisp. :)

## Quick Example

```lisp
>>> (defvar x 10)
x

>>> (defvar y 20)
y

>>> (* x 3)
30

>>> (< x y)
t

>>> (if (< x y) "smaller" "larger")
"smaller"

>>> (defun square (n) (* n n))
square

>>> (square 5)
25

>>> (message "hello")
"hello"
```

## Requirements

Python 3. No third-party dependencies — only the standard library.

## Usage

### REPL

Start the REPL:

```bash
python hith.py
```

Type expressions at the `>>> ` prompt. Type `exit` to quit.

### Run a Hith Script

```bash
python hith.py script
```

Any extra command-line arguments are passed through and available inside the script as `command-line-args` — a list whose first element is the script's own path, followed by whatever else you passed:

```bash
python hith.py greet friend
```

```bash
(message (nth 1 command-line-args))
```

Output:

```bash
friend
```

### Use Hith from Python Code

```python
from evaluate import Evaluator

evaluator = Evaluator()

result = evaluator.evaluate("(+ 1 2)")
print(result.value)
```

Output:

```bash
3
```

Every value `evaluate` returns wraps its underlying Python value in `.value` — except lists, which come back as plain Python lists of wrapped values:

```python
result = evaluator.evaluate("(list 1 2 3)")
print([item.value for item in result])
```

Output:

```bash
[1, 2, 3]
```

## Language Overview

### Values

Hith has five kinds of value:

| Type | Example | Notes |
| --- | --- | --- |
| Integer | `42` | |
| Float | `3.14159` | Mixing an Integer and a Float in one expression promotes the result to Float |
| String | `"Hello, world!"` | Always double-quoted |
| Symbol | `x`, `my-var`, `square` | Names of variables, functions, or quoted data |
| List | `(1 2 3)`, `'(a b c)` | A parenthesized, space-separated sequence |

```lisp
>>> 42
42

>>> 3.14159
3.14159

>>> "Hello, world!"
"Hello, world!"
```

There's no separate boolean type. Truth is `t`; Every value other than `nil` is truthy in a conditional — numbers, strings, and non-empty lists included:
```lisp
>>> (if nil 1 2)
2

>>> (if "anything" 1 2)
1
```

### Arithmetic

`+`, `-`, `*`, and `/` each take exactly two arguments — nest calls to combine more than two values:

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

>>> x
10

>>> (symbol-value (quote x))
10

>>> (setq z 40)
z

>>> z
40

>>> (symbol-value 'undefined-var)
nil
```

`defvar` and `setq` both return the variable's *name* (as a symbol), not its value — keep that in mind if you're chaining expressions together.

They also differ in an important way: `defvar` always creates (or overwrites) a variable in the *current* scope, even if a variable with the same name already exists further out. `setq` instead looks for an existing binding — starting locally and searching outward — and updates that binding in place; only if no binding exists anywhere does it create a new local one. In practice: use `defvar` to introduce a variable, and `setq` to mutate one you expect already exists, however far out it lives. (This is exactly how the loop variable in `for`/`range`/`while`, below, ends up visible after the loop finishes.)

### Printing

```lisp
>>> (message "hello")
"hello"
```

`message` formats a string, prints it (without surrounding quotes) to standard out, and returns the formatted string. `format` does the same formatting but only returns the string — it never prints:

```lisp
>>> (format "test %s test" "value")
"test value test"

>>> (format "test %s test" (+ 1 2))
"test 3 test"

>>> (format "%s and %s" 1 "two")
"1 and two"
```

Each `%s` in the template is replaced, left to right, by the corresponding argument.

### Comparisons

`>`, `<`, `>=`, `<=`, and `eq` each take exactly two arguments and return `t` or `nil`:

```lisp
>>> (> 2 1)
t

>>> (< 2 1)
nil

>>> (>= 2 2)
t

>>> (<= 3 2)
nil

>>> (eq 1 1)
t

>>> (eq (< 1 2) (> 2 1))
t
```

### Conditionals

```lisp
>>> (if t 1 2)
1

>>> (if False 1 2)
2

>>> (if (< 1 2) (+ 1 2) (+ 2 3))
3

>>> (if False 1)
nil
```

An `if` with no else-branch returns `nil` when the test is false.

For more than two branches, use `cond`. Each clause is a test paired with a result; the first clause whose test is truthy "wins," and a final clause of `t` acts as the default:

```lisp
(defun check-value (x)
  (cond
    ((< x 0) "negative")
    ((eq x 0) "zero")
    ((eq x 1) "exactly one")
    (t "something else")))
```

```lisp
>>> (check-value -1)
"negative"

>>> (check-value 1)
"exactly one"

>>> (check-value 99)
"something else"
```

### Loops

Hith has four looping constructs. All of them run their body — which may be more than one expression — once per iteration, in order.

`while` re-checks its condition before every iteration:

```lisp
(defvar count 0)
(while (< count 5)
  (setq count (+ count 1)))
```
`count` is `5` afterward.

`for` is a classic init/condition/update loop:

```lisp
(defvar total 0)
(for i 0 (< i 10) (setq i (+ i 1))
  (setq total (+ total i)))
```
`total` is `45` afterward, and `i` itself is left holding `10`.

`range` is a shorthand for counting from a lower bound up to (but not including) an upper bound, stepping by 1 automatically:

```lisp
(defvar total 0)
(range i 0 10
  (setq total (+ total i)))
```
Also `45` — with `i` left holding `10`.

`foreach` walks the elements of a list:

```lisp
(defvar total 0)
(foreach item (list 1 2 3 4 5)
  (setq total (+ total item)))
```
`total` is `15` afterward. Reassigning the loop variable inside the body doesn't mutate the original list.

All four loops can be nested, and all of them leave their loop variable (and anything else touched via `setq`) accessible after the loop ends.

### Lists

A list is written as parenthesized, space-separated items. Prefixing an expression with `'` is shorthand for wrapping it in `quote` — it returns the expression as literal data instead of evaluating it as a function call:

```lisp
>>> (defvar nums (list 1 2 3))
nums

>>> (length nums)
3

>>> (nth 0 nums)
1

>>> (nth 2 nums)
3

>>> (car nums)
1
```

```lisp
>>> (defvar letters '(a b c))
letters

>>> (nth 1 letters)
b

>>> (quote hello)
hello
```

`cons` prepends an item to a list, and `cdr` returns everything after the first item:

```lisp
>>> (defvar more (cons 0 nums))
more

>>> (length more)
4

>>> (nth 0 more)
0
```

`length` also works on strings:

```lisp
>>> (length "hello")
5
```

`nth` returns `nil` for an out-of-range index, and `car` returns `nil` for an empty list.

### Functions

Functions are defined with `defun`. A function body can contain several expressions, evaluated in order, with the last one's value returned:

```lisp
(defun max2 (a b)
  (if (> a b) a b))
```

```lisp
>>> (max2 10 4)
10
```

```lisp
(defun multi-step (x y)
  (setq total (+ x y))
  (setq total (* total y))
  (+ total y))
```

```lisp
>>> (multi-step 2 3)
18
```

Functions run in their own lexical environment: parameters are local to the call, while outer variables and functions remain reachable. Defining a function inside another function creates a closure — the inner function can see the outer function's variables, but the inner function itself only exists for the duration of that call and isn't visible globally:

```lisp
(defun outer-func (x)
  (defun inner-func (x) (+ x 1))
  (+ x (inner-func 10)))
```

```lisp
>>> (outer-func 5)
16

>>> (inner-func 10)
Function with name inner-func is undefined
```

A parameter list can end with `&rest name` to collect any remaining arguments into a list:

```lisp
(defun my-list (&rest items) items)
```

```lisp
>>> (defvar result (my-list 1 2 3))
result

>>> (length result)
3
```

You can also write recursive functions in the usual way:

```lisp
(defun factorial (n)
  (if (<= n 1)
      1
      (* n (factorial (- n 1)))))
```

```lisp
>>> (factorial 5)
120
```

### Macros

Macros are defined with `defmacro`. Unlike a function, a macro receives its arguments as unevaluated code, and instead of computing a value it returns a new piece of code, which is then evaluated in its place. Backquote (a leading backtick) quotes a template while still allowing two escapes inside it: `,` evaluates a single piece normally, and `,@` evaluates a piece that must be a list and splices its items in.

A minimal example:

```lisp
(defmacro double (x) `(* 2 ,x))
```

```lisp
>>> (double 5)
10
```

A more complete one, combining `&rest` with `,@` to splice a whole macro body into a `progn`:

```lisp
(defmacro my-when (test &rest body)
  `(if ,test (progn ,@body) False))
```

```lisp
>>> (defvar x 10)
x

>>> (my-when (> x 5)
      (setq x (+ x 1))
      (setq x (* x 2))
      x)
22

>>> x
22
```

### Symbols

```lisp
>>> (make-symbol "x")
x
```

`make-symbol` builds a symbol with exactly the name you give it. `gensym` instead manufactures a symbol guaranteed to be fresh — handy inside macros, to avoid accidentally colliding with a name already in use:

```lisp
>>> (gensym)
#:G1

>>> (gensym)
#:G2
```

### Type Predicates

| Predicate | True for |
| --- | --- |
| `atom` | integers, floats, strings, and symbols — anything that isn't a list |
| `intp` | integers |
| `floatp` | floats |
| `stringp` | strings |
| `symbolp` | symbols |

```lisp
>>> (intp 10)
t

>>> (floatp 12.23)
t

>>> (stringp "test")
t

>>> (symbolp (quote x))
t

>>> (defvar x 10)
x

>>> (atom x)
t
```

### Randomness

```lisp
>>> (floatp (random))
t

>>> (intp (randrange 0 5))
t
```

`random` returns a float in `[0, 1)`. `randrange` returns a random integer for a given range, the same way Python's `random.randrange` does. `choice` picks a uniformly random element from a list, or `nil` for an empty one:

```lisp
>>> (defvar options '(a b c))
options

>>> (choice options)
b

>>> (choice '())
nil
```

### Files

```lisp
>>> (defvar lines (file-read-lines "notes.txt"))
lines

>>> (nth 0 lines)
"first"
```

`file-read-lines` reads a file from disk and returns its lines as a list of strings.

### Sequencing with progn

`progn` evaluates a series of expressions in order and returns the last one's value — useful anywhere the grammar expects a single expression but you need several steps:

```lisp
>>> (progn (setq a 10) (setq b 20) (+ a b))
30

>>> (progn)
nil
```

### Miscellaneous

```lisp
>>> (round 4.6)
5
```

`round` rounds to the nearest integer. `exit` — as a call, `(exit)`, or just by typing `exit` at the REPL prompt — ends the program.

## Quick Reference

### Special Forms and Core Constructs

| Form | Kind | Description |
| --- | --- | --- |
| `quote` / `'` | special form | Returns its argument unevaluated |
| backquote (leading backtick) | special form | Quotes a template, allowing `,`/`,@` escapes inside it |
| `,` unquote | backquote syntax | Evaluates one piece inside a backquoted template |
| `,@` unquote-splice | backquote syntax | Evaluates a list and splices its items into a backquoted template |
| `defvar` | special form | Defines/overwrites a variable in the current scope |
| `setq` | special form | Updates an existing variable wherever it's bound, else creates one locally |
| `symbol-value` | special form | Looks up a symbol's value (`nil` if undefined) |
| `if` | special form | `(if test then [else])` |
| `cond` | macro | Multi-branch conditional; a `t` clause acts as the default |
| `defun` | special form | Defines a function; supports `&rest` |
| `defmacro` | special form | Defines a macro; supports `&rest` |
| `while` | macro | `(while test body...)` |
| `for` | macro | `(for var init test update body...)` |
| `range` | macro | `(range var lower upper body...)` |
| `foreach` | macro | `(foreach var list body...)` |
| `progn` | special form | Evaluates a sequence, returns the last value |
| `format` | special form | Builds a formatted string, does not print |
| `message` | special form | Formats, prints, and returns a string |
| `length` | special form | Length of a string or list |

### Built-in Functions

| Function | Description |
| --- | --- |
| `+` `-` `*` `/` | Arithmetic (2 arguments each) |
| `>` `<` `>=` `<=` `eq` | Comparisons (2 arguments each); return `t` or `nil` |
| `list` | Builds a list from its arguments |
| `cons` | Prepends an item to a list |
| `car` | First item of a list (`nil` if empty) |
| `cdr` | Everything after the first item of a list |
| `nth` | Item at a 0-based index (`nil` if out of range) |
| `atom` `intp` `floatp` `stringp` `symbolp` | Type predicates |
| `make-symbol` | Builds a symbol from a string |
| `gensym` | Generates a fresh, unique symbol |
| `random` | Random float in `[0, 1)` |
| `randrange` | Random integer in a range |
| `choice` | Random element of a list (`nil` if empty) |
| `round` | Rounds to the nearest integer |
| `file-read-lines` | Reads a file into a list of line-strings |
| `exit` | Ends the program |

## Architecture

The interpreter has three stages, plus a small self-hosted standard library.

### Lexer

Converts source code into tokens.

Input: `(+ 1 2)`
Output: `['(', '+', '1', '2', ')']`

### Parser

Converts tokens into an Abstract Syntax Tree.

Output (conceptually): `["+", 1, 2]`

### Evaluator

Recursively evaluates the AST. `quote`, `backquote`, `defvar`, `setq`, `symbol-value`, `if`, `defun`, `defmacro`, `format`, `message`, `length`, and `progn` are special forms and receive their arguments unevaluated; ordinary functions evaluate all of their arguments first. Macros are expanded once per call site into a new piece of code, which is then evaluated in the calling environment.

Evaluation happens inside an `Env` object, and environments nest through parent links. A user-defined function creates a new environment whose parent is the environment the function was *defined* in (not the one it's *called* from), which is what gives Hith lexical scoping and closures.

### Standard Library

Not everything lives in the Python evaluator. Features like `cond`, `while`, `for`, `range`, `foreach`, `randrange`, `choice`, and `gensym` are themselves written in Hith, using `defmacro`/`defun`, and are loaded automatically from the `libs/` directory the moment an `Evaluator` is created.

## Running Tests

Run all tests:

```lisp
python -m unittest discover
```

or:

```lisp
make test
```

Or run an individual test file:

```lisp
python test_lexer.py
```

## Current Limitations

- Limited error handling.
- No comment syntax — there's currently no way to annotate a Hith source file.
- Arithmetic and comparison operators are binary only (exactly two arguments); nest calls for chains of more than two values.
- The REPL prints a result by reading its `.value`, so an expression that evaluates to a bare list (`list`, `cons`, `cdr`, or a quoted list) won't print at the `>>> ` prompt. Assign it to a variable and inspect it with `nth`/`length`, or drive it from Python via `evaluate(...)` directly.
