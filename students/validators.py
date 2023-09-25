from django.core.exceptions import ValidationError


def validate_file_size(value):
    filesize = value.size

    if filesize > 500000:
        raise ValidationError("Le poids de la photo ne doit pas dépasser 500kB.")
    return value


def check_special_characters(value):
    special_characters = [
        "~",
        ":",
        "'",
        "+",
        "[",
        "\\",
        "@",
        "^",
        "{",
        "%",
        "(",
        "-",
        '"',
        "*",
        "|",
        ",",
        "&",
        "<",
        "`",
        "}",
        ".",
        "=",
        "]",
        "!",
        ">",
        ";",
        "?",
        "#",
        "$",
        ")",
        "/",
    ]
    for special_character in special_characters:
        if special_character in value:
            raise ValidationError("Les caractères spéciaux sont interdits.")
    return value


def check_special_characters_limited(value):
    special_characters = [
        ">",
        "<",
    ]
    for special_character in special_characters:
        if special_character in value:
            raise ValidationError('Les caractères "<" et ">" sont interdits.')
    return value
