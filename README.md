# Hith

A Lisp interpreter, written from scratch in Python. Hith has s-expression syntax, lexical scoping with closures, macros with quasiquotation, and a small standard library of loops, logical operators, and string/list helpers written in Hith itself.

Hith supports:

- Arithmetic and comparison operators
- `t` / `nil` as true and false
- Variables (`defvar`, `setq`) and symbol lookup
- Integers and floats (mixing the two promotes to float)
- Strings
- Lists, and list operations (`list`, `cons`, `car`, `cdr`, `nth`, `length`, `push`, `reverse`, `append`)
- Conditionals (`if`, `cond`)
- Logical operators (`and`, `or`, `not`, `unless`)
- Loops (`while`, `for`, `range`, `foreach`, `repeat`)
- User-defined functions (`defun`) with multi-expression bodies and `&rest` parameters
- Calling functions indirectly with `funcall`
- Lexical scoping and closures
- Macros (`defmacro`) with backquote/unquote/unquote-splice
- Type predicates (`atom?`, `int?`, `float?`, `string?`, `symbol?`)
- Regular expressions and string helpers (`string-match`, `string-to-number`, `substring`, `split-string`, `string-contains`)
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
  - [Logical Operators](#logical-operators)
  - [Loops](#loops)
  - [Lists](#lists)
  - [Functions](#functions)
  - [Macros](#macros)
  - [Symbols](#symbols)
  - [Type Predicates](#type-predicates)
  - [Regex and Strings](#regex-and-strings)
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

>>> (defmacro my-when (test &rest body) `(if ,test (progn ,@body) nil))
my-when

>>> (my-when (> x 5) (setq x (+ x 1)) (* x 2))
22
```

## Requirements

Python 3. No third-party dependencies, only the standard library.

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

Any extra command-line arguments are passed through and available
inside the script as `command-line-args`. A list whose first element is
the script's own path, followed by whatever else you passed:

```bash
python hith.py greet friend
```

```lisp
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

Every value `evaluate` returns wraps its underlying Python value in
`.value` except lists, which come back as plain Python lists of
wrapped values:

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

There's no separate boolean type. Truth is `t`; every value other than
`nil` is truthy in a conditional including numbers, strings, and
non-empty lists:

```lisp
>>> (if nil 1 2)
2

>>> (if "anything" 1 2)
1
```

### Arithmetic

`+`, `-`, `*`, and `/` each take exactly two arguments. Nest calls to
combine more than two values:

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

`defvar` and `setq` both return the variable's *name* (as a symbol),
not its value. Keep that in mind if you're chaining expressions
together.

They also differ in an important way: `defvar` always creates (or
overwrites) a variable in the *current* scope, even if a variable with
the same name already exists further out. `setq` instead looks for an
existing binding, starting locally and searching outward, and updates
that binding in place; only if no binding exists anywhere does it
create a new local one. In practice: use `defvar` to introduce a
variable, and `setq` to mutate one you expect already exists, however
far out it lives. (This is exactly how the loop variable in
`for`/`range`/`while`, below, ends up visible after the loop
finishes.)

### Printing

```lisp
>>> (message "hello")
"hello"
```

`message` formats a string, prints it (without surrounding quotes) to
standard out, and returns the formatted string. `format` does the same
formatting but only returns the string:

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

>>> (if nil 1 2)
2

>>> (if (< 1 2) (+ 1 2) (+ 2 3))
3

>>> (if nil 1)
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

### Logical Operators

`not` inverts a value to `t` or `nil`. `and` and `or` short-circuit and
each take any number of arguments:

```lisp
>>> (not nil)
t

>>> (not t)
nil
```

`and` evaluates its arguments left to right and returns the value of
the last one, unless one of them is `nil`, in which case it stops
early and returns `nil`. With no arguments, it returns `t`:

```lisp
>>> (and)
t

>>> (and t 1 (+ 2 3))
5

>>> (and t nil (+ 2 3))
nil
```

`or` returns the value of the first truthy argument, stopping as soon
as it finds one. With no arguments, or if every argument is `nil`, it
returns `nil`:

```lisp
>>> (or)
nil

>>> (or (> 1 1) (+ 1 2))
3

>>> (or (> 1 1) (> 1 1))
nil
```

`unless` is the inverse of a one-armed `if`; it runs its body only when
the condition is falsy:

```lisp
>>> (unless (> 1 2) (+ 3 2))
5

>>> (unless (> 2 1) (+ 3 2))
nil
```

### Loops

Hith has five looping constructs. All of them run their body, which may be more than one expression, once per iteration, in order.

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

Also `45` with `i` left holding `10`.

`foreach` walks the elements of a list:

```lisp
(defvar total 0)
(foreach item (list 1 2 3 4 5)
  (setq total (+ total item)))
```
`total` is `15` afterward. Reassigning the loop variable inside the body doesn't mutate the original list.

`repeat` runs its body a fixed number of times, without giving you access to a loop variable:

```lisp
(defvar hits 0)
(repeat 3
  (setq hits (+ hits 1)))
```
`hits` is `3` afterward.

All five loops can be nested, and all of them leave their loop variable (and anything else touched via `setq`) accessible after the loop ends.

### Lists

A list is written as parenthesized, space-separated items. Prefixing
an expression with `'` is shorthand for wrapping it in `quote`. It
returns the expression as literal data instead of evaluating it as a
function call:

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

`push` and `append` build on `cons` to add an item to the front or the
back of a list, and `reverse` flips one around, all returning new
lists rather than mutating the original:

```lisp
>>> (defvar nums (list 1 2 3))
nums

>>> (push 0 nums)
(0 1 2 3)

>>> (append 4 nums)
(1 2 3 4)

>>> (reverse nums)
(3 2 1)
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

Functions run in their own lexical environment: parameters are local
to the call, while outer variables and functions remain
reachable. Defining a function inside another function creates a
closure. The inner function can see the outer function's variables,
but the inner function itself only exists for the duration of that
call and isn't visible globally:

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

Functions can also be called indirectly with `funcall`, either by
symbol or by a variable that holds one. This is handy for passing a
function around as a value:

```lisp
>>> (funcall + 1 2)
3

>>> (defvar my-op '+)
my-op

>>> (funcall my-op 1 2)
3
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
  `(if ,test (progn ,@body) nil))
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

`make-symbol` builds a symbol with exactly the name you give
it. `gensym` instead manufactures a symbol guaranteed to be
fresh. This is handy inside macros to avoid accidentally colliding
with a name already in use:

```lisp
>>> (gensym)
#:G1

>>> (gensym)
#:G2
```

### Type Predicates

| Predicate | True for |
| --- | --- |
| `atom?` | integers, floats, strings, and symbols. Anything that isn't a list |
| `int?` | integers |
| `float?` | floats |
| `string?` | strings |
| `symbol?` | symbols |

```lisp
>>> (int? 10)
t

>>> (float? 12.23)
t

>>> (string? "test")
t

>>> (symbol? (quote x))
t

>>> (defvar x 10)
x

>>> (atom? x)
t
```

### Regex and Strings

`string-match` searches a string for a regular expression pattern and
returns the index of the first match, or `nil` if there's no match.
Regex metacharacters like `+`, `.`, `(`, and `)` need to be escaped
with a backslash to be matched literally:

```lisp
>>> (string-match "test" "e")
1

>>> (string-match "test" "z")
nil

>>> (string-match "a+b" "\\+")
1
```

`string-to-number` parses a string into an Integer or a Float, or
returns `nil` if it isn't a valid number:

```lisp
>>> (string-to-number "10")
10

>>> (string-to-number "10.55")
10.55

>>> (string-to-number "not a number")
nil
```

Built on top of `string-match` and `nth`, the standard library adds a
few more string helpers. `substring` extracts the characters between
two indices, `split-string` breaks a string apart on every occurrence
of a separator, and `string-contains` reports whether a match exists
at all:

```lisp
>>> (substring "test" 0 2)
"te"

>>> (split-string "test test" "e")
("t" "st t" "st")

>>> (string-contains "test" "es")
t
```

### Randomness

```lisp
>>> (float? (random))
t

>>> (int? (randrange 0 5))
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

`progn` evaluates a series of expressions in order and returns the
last one's value. This is useful anywhere the grammar expects a single
expression but you need several steps:

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

`round` rounds to the nearest integer. `(exit)` or just type `exit` at
the REPL prompt to exit the program.

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
| `and` | macro | Short-circuiting logical and |
| `or` | macro | Short-circuiting logical or |
| `unless` | macro | Runs its body only when the test is falsy |
| `defun` | special form | Defines a function; supports `&rest` |
| `defmacro` | special form | Defines a macro; supports `&rest` |
| `while` | macro | `(while test body...)` |
| `for` | macro | `(for var init test update body...)` |
| `range` | macro | `(range var lower upper body...)` |
| `foreach` | macro | `(foreach var list body...)` |
| `repeat` | macro | `(repeat n body...)` |
| `progn` | special form | Evaluates a sequence, returns the last value |
| `funcall` | special form | Calls a function by symbol, including one held in a variable |
| `format` | special form | Builds a formatted string, does not print |
| `message` | special form | Formats, prints, and returns a string |
| `length` | special form | Length of a string or list |

### Built-in Functions

| Function | Description |
| --- | --- |
| `+` `-` `*` `/` | Arithmetic (2 arguments each) |
| `>` `<` `>=` `<=` `eq` | Comparisons (2 arguments each); return `t` or `nil` |
| `not` | Logical negation |
| `list` | Builds a list from its arguments |
| `cons` | Prepends an item to a list |
| `car` | First item of a list (`nil` if empty) |
| `cdr` | Everything after the first item of a list |
| `nth` | Item at a 0-based index (`nil` if out of range); works on strings too |
| `push` | Prepends an item to a list (standard library) |
| `append` | Appends an item to the end of a list (standard library) |
| `reverse` | Reverses a list (standard library) |
| `atom?` `int?` `float?` `string?` `symbol?` | Type predicates |
| `make-symbol` | Builds a symbol from a string |
| `gensym` | Generates a fresh, unique symbol |
| `string-match` | Searches a string for a regex pattern, returns the match index or `nil` |
| `string-to-number` | Parses a string into an Integer or Float, or `nil` |
| `substring` | Extracts a substring between two indices (standard library) |
| `split-string` | Splits a string on every occurrence of a separator (standard library) |
| `string-contains` | Checks whether a substring/pattern matches (standard library) |
| `random` | Random float in `[0, 1)` |
| `randrange` | Random integer in a range (standard library) |
| `choice` | Random element of a list, `nil` if empty (standard library) |
| `round` | Rounds to the nearest integer |
| `file-read-lines` | Reads a file into a list of line-strings |
| `exit` | Ends the program |

## Architecture

The interpreter has three stages, plus a small self-hosted standard library.

### Lexer

Converts source code into tokens, including the `'`, `` ` ``, `,`, and `,@` quoting markers.

Input: `(+ 1 2)`
Output: `['(', '+', '1', '2', ')']`

### Parser

Converts tokens into an Abstract Syntax Tree, attaching any pending quote/backquote/unquote/unquote-splice markers to the form that follows them.

Output (conceptually): `["+", 1, 2]`

### Evaluator

Recursively evaluates the AST. `quote`, `backquote`, `defvar`, `setq`, `symbol-value`, `if`, `defun`, `defmacro`, `format`, `message`, `length`, `progn`, and `funcall` are special forms and receive their arguments unevaluated; ordinary functions evaluate all of their arguments first. Macros are expanded once per call site into a new piece of code, which is then evaluated in the calling environment.

Evaluation happens inside an `Env` object, and environments nest through parent links. A user-defined function or macro creates a new environment whose parent is the environment it was *defined* in (not the one it's *called* from), which is what gives Hith lexical scoping and closures. Function and macro parameter lists may end with `&rest name` to collect any remaining arguments into a list.

### Standard Library

Not everything lives in the Python evaluator. A number of features are themselves written in Hith, using `defun`/`defmacro`, and are loaded automatically from the `libs/` directory the moment an `Evaluator` is created:

| File | Provides |
| --- | --- |
| `core.ht` | `gensym` |
| `list.ht` | `push`, `reverse`, `append` |
| `logic.ht` | `cond`, `and`, `or`, `not`, `unless` |
| `loops.ht` | `while`, `for`, `range`, `foreach`, `repeat` |
| `random.ht` | `randrange`, `choice` |
| `string.ht` | `substring`, `string-contains`, `split-string` |

## Running Tests

Run all tests:

```bash
python -m unittest discover
```

or:

```bash
make test
```

Or run an individual test file:

```bash
python test_lexer.py
```
