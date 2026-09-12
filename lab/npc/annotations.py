
function_mapping = {}

def function():
    def wrapper(f):
        function_mapping[f.__name__.lower()] = f
        return f
    return wrapper