import re


def get_account_key(con_str: str) -> str:
    pattern = r"AccountKey=(?P<account_key>[\w=+/]+);"
    compile_pattern = re.compile(pattern)
    match = compile_pattern.search(con_str)

    if not match:
        raise RuntimeError("Incorrect azure connection string, could not find account_key.")

    return match.group("account_key")
