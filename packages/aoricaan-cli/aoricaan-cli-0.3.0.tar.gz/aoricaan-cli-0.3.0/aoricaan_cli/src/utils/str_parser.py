def snake_case_or_kebab_case_to_pascal_case(any_string):
    """
    Converts any string to PascalCase.

    any_string: str

    Returns: str
    """
    return any_string.replace('-', ' ').replace("_", " ").title().replace(" ", "")
