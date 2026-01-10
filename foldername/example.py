def register(commands):
    def cmd_hello(args):
        if args:
            print("Hello,", " ".join(args))
        else:
            print("Hello from plugin 👋")
    commands["hello"] = cmd_hello
