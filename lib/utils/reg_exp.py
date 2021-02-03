import re

SPECIAL_CHARACER_REGEX = re.compile(r"[^A-Za-z0-9]")


class RegExp:
    @staticmethod
    def replace_special_characters(string: str, replacement: str) -> str:
        return SPECIAL_CHARACER_REGEX.sub(replacement, string)
