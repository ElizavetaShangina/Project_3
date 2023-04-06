def dec(func):
    def dec2(*args, **kwargs):
        print("hello")
        return func(*args, **kwargs)
    return dec2


@dec
def smt(*args, **kwargs):
    return args, kwargs


print(smt("hello", end="ti"))