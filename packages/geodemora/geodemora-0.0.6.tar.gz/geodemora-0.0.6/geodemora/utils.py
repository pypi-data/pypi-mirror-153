def random_string(string_length=3, use_seed = False):
    """Generates a random string of fixed length.
    Args:
        string_length (int, optional): Fixed length. Defaults to 3.
    Returns:
        str: A random string
    """
    import random
    import string

    if use_seed:
        random.seed(1001)
    letters = string.ascii_lowercase
    return "".join(random.choice(letters) for i in range(string_length))

def add(x, y):
    """Add two given numbers

    Args:
        x (int/float): _description_
        y (int/float): _description_
    """
    return x + y

def subtract(x, y):
    """Subtract y from x.

    Args:
        x (int/float): _description_
        y (int/float): _description_
    """
    return x - y

def multiply(x, y):
    """Multiply two numbers

    Args:
        x (int/float): _description_
        y (int/float): _description_
    """
    return x * y
    