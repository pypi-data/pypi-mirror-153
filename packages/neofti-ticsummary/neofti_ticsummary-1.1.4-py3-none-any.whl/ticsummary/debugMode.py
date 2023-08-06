import sys

def checkDebugMode():
    gettrace = getattr(sys, 'gettrace', None)
    if gettrace is None:
        print('Debug mode is disabled')
    elif gettrace():
        print('Debug mode is enabled')
    else:
        print("Debug mode is unknow")

def conditionalDebugDecorator(dec):
    def decorator(func):
        if not checkDebugMode():
            # Return the function unchanged, not decorated.
            return func
        return dec(func)
    return decorator