import re

CHAR = "\u00a7"  # Format char
MAP = {
    "0": "\033[0m\033[30m",
    "1": "\033[0m\033[34m",
    "2": "\033[0m\033[32m",
    "3": "\033[0m\033[36m",
    "4": "\033[0m\033[31m",
    "5": "\033[0m\033[36m",
    "6": "\033[0m\033[33m",
    "7": "\033[0m\033[38;5;246m",
    "8": "\033[0m\033[38;5;243m",
    "9": "\033[0m\033[34;1m",
    "a": "\033[0m\033[32;1m",
    "b": "\033[0m\033[36;1m",
    "c": "\033[0m\033[31;1m",
    "d": "\033[0m\033[35;1m",
    "e": "\033[0m\033[33;1m",
    "f": "\033[0m\033[37;1m",
    "l": "\033[1m",
    "k": "\033[5m",
    "m": "\033[9m",
    "n": "\033[4m",
    "o": "\033[3m",
    "r": "\033[0m",
}  # Mapping format chars with ASCII values


def clean(text: str) -> str:
    pattern = re.compile(f"{re.escape(CHAR)}([{ ''.join(MAP.keys()) }])")
    cleaned = pattern.sub("", text)
    cleaned = cleaned.lstrip("[Lvl {LVL}] ")
    return cleaned
