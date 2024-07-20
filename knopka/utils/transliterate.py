CYRILLIC_LATIN = {
    "А": "A",
    "Б": "B",
    "В": "V",
    "Г": "G",
    "Д": "D",
    "Е": "E",
    "Ё": "E",
    "Ж": "Zh",
    "З": "Z",
    "И": "I",
    "Й": "Y",
    "К": "K",
    "Л": "L",
    "М": "M",
    "Н": "N",
    "О": "O",
    "П": "P",
    "Р": "R",
    "С": "S",
    "Т": "T",
    "У": "U",
    "Ф": "F",
    "Х": "Kh",
    "Ц": "Ts",
    "Ч": "Ch",
    "Ш": "Sh",
    "Щ": "Shch",
    "Ы": "Y",
    "Э": "E",
    "Ю": "Yu",
    "Я": "Ya",
    "а": "a",
    "б": "b",
    "в": "v",
    "г": "g",
    "д": "d",
    "е": "e",
    "ё": "e",
    "ж": "zh",
    "з": "z",
    "и": "i",
    "й": "y",
    "к": "k",
    "л": "l",
    "м": "m",
    "н": "n",
    "о": "o",
    "п": "p",
    "р": "r",
    "с": "s",
    "т": "t",
    "у": "u",
    "ф": "f",
    "х": "kh",
    "ц": "ts",
    "ч": "ch",
    "ш": "sh",
    "щ": "shch",
    "ы": "y",
    "э": "e",
    "ю": "yu",
    "я": "ya",
}


def transliterate(text: str) -> str:
    """Simple func to transliterate"""

    result: str = ""
    for char in str(text).strip():
        if char not in CYRILLIC_LATIN.keys():
            continue

        result += CYRILLIC_LATIN[char]

    return result


def transliterate_lower(text: str) -> str:
    """Simple func to transliterate (and lower!)"""

    return transliterate(text=text).lower()
