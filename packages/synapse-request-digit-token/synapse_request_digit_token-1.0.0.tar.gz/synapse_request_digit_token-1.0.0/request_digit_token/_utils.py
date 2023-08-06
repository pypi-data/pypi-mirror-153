import secrets
import string


def random_digit_string(length: int) -> str:
    return "".join(secrets.choice(string.digits) for _ in range(length))
