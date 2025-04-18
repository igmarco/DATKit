import ast


def parse_value(value):
    """
    Attempts to evaluate the given value as a Python literal.

    Parameters
    ----------
    value : str
        A string representing a Python literal (e.g., a number, list, dictionary, etc.) that should be evaluated.

    Returns
    ----------
    literal or original
        If the evaluation with ast.literal_eval is successful, returns the evaluated literal.
        Otherwise, returns the original value.
    """
    try:
        return ast.literal_eval(value)
    except (ValueError, SyntaxError):
        return value