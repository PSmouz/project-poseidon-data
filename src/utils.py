import re


def extract_materials(value):
    # Regex pattern to match percentage and material
    pattern = re.compile(
        r"(\d{1,3}%)\s*([\w\s]+?)(?=(?:\s*,|\s*<|\s*(?:\d{1,3}%|$)))"
    )
    # Extract matches from the value
    matches = pattern.findall(value)
    result = [
        f"{percentage} {material.lower()}" for percentage, material in matches
    ]
    return result
