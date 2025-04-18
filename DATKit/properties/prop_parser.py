import ast


def parse_value(value):
    try:
        # Intentar evaluar el valor como un literal (números, listas, etc.)
        return ast.literal_eval(value)
    except (ValueError, SyntaxError):
        # Si falla, devolverlo como string
        return value
