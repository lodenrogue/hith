from evaluate import evaluate


def start_repl():
    print("Welcome to Hiss. A lisp written in Python.")
    print("Type exit to quit")

    while True:
        exp = input(">>> ")

        if exp == "exit":
            exit()
        else:
            print(evaluate(exp))
    

if __name__ == "__main__":
    start_repl()
