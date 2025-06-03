import secrets


def shortid(length=6):
    # Readable, unambiguous characters for short IDs
    alphabet = "23456789abcdefghjkmnprstvwyz"  # 27 characters

    id = ""

    while len(id) < length:
        id += secrets.choice(alphabet)

    return id
