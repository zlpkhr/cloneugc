import secrets


def shortid(length=6):
    # Optimized for URL readability and UX:
    # - Removed visually similar: 0/o, 1/l, i, u
    # - Removed pronunciation issues: q (needs 'u'), x (uncommon)
    # - Kept vowels a,e for readability
    # - All remaining chars are keyboard-friendly and clear
    alphabet = "23456789abcdefghjkmnprstvwyz"  # 27 characters

    return "".join(secrets.choice(alphabet) for _ in range(length))
