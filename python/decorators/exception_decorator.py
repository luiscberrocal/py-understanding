# PythonDecorators/decorator_function_with_arguments.py


def decorator_function_with_arguments(arg1, arg2, arg3):
    def wrap(f):
        print("Inside wrap()")

        def wrapped_f(*args):
            print(f"Inside wrapped_f() {f.__name__}")
            print("Decorator arguments:", arg1, arg2, arg3)
            f(*args)
            print(f"After f(*args) {args}")

        return wrapped_f

    return wrap


class WrapperException(Exception):
    """Wrapper exception for the Felix Pago SDK."""
    pass


def exception_decorator(**kwargs):
    def wrap(f):
        print("Inside wrap()")
        try:
            def wrapped_f(*args):
                print(f"Inside wrapped_f() {f.__name__}")
                print("Decorator arguments:", args, kwargs)
                f(*args)
                print(f"After f(*args) {args}")
                return wrapped_f
        except ValueError as e:
            error_message = f"Value error while {kwargs.get('process')}. Error: {e}."
            raise WrapperException(error_message)
        except Exception as e:
            error_message = f"Unexpected error while {kwargs.get('process')}. Type: {e.__class__.__name__} error: {e}."
            raise WrapperException(error_message)

    return wrap


@decorator_function_with_arguments("hello", "world", 42)
def sayHello(a1, a2, a3, a4):
    print('sayHello arguments:', a1, a2, a3, a4)


@exception_decorator(process="calling the function")
def process_request():
    try:
        print("Processing request")
        raise ValueError("Value error while processing request")
    except WrapperException as e:
        print(f"Wrapper exception: {e}")

def main():
    print("After decoration")

    print("Preparing to call sayHello()")
    sayHello("say", "hello", "argument", "list")
    print('-' * 100)
    print("after first sayHello() call")
    sayHello("a", "different", "set of", "arguments")
    print("after second sayHello() call")


if __name__ == '__main__':
    process_request()