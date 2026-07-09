import sys
import os
import contextlib
from evaluate import Evaluator, Env, Variables

evaluate = Evaluator().evaluate


def run_script(path, arg_list):
    with open(path, "r") as f:
        args = " ".join([f'"{arg}"' for arg in arg_list])
        evaluate(f'(defvar command-line-args (quote ({args})))')
        evaluate(f.read())


def start_repl():
    print("Welcome to Hith. A lisp written in Python.")
    print("Type exit to quit.")

    while True:
        try:
            exp = input(">>> ")

            if exp == "exit":
                exit()
            else:
                # suppress prints from evaluation
                with contextlib.redirect_stdout(open(os.devnull, 'w')):
                    result = evaluate(exp)

                if isinstance(result, list):
                    print([item.value for item in result])
                else:
                    print(result.value)
        except Exception as e:
            print(e)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        run_script(sys.argv[1], sys.argv[1:])
    else:
        start_repl()
