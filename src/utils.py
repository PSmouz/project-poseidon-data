import re


def extract_materials(value):
    """
    Passes tests for:
     - Teveo

    Args:
        value:

    Returns:

    """
    # Regex pattern to match percentage and material
    pattern = re.compile(
        r"(\d{1,3}\s?%)\s*([\w\s]+?)(?=(?:\s*,|\s*<|\s*(?:\d{1,"
        r"3}\s?%|$|\s*[&.]|\s*und)))"
    )

    # Extract matches from the value
    matches = pattern.findall(value)
    # Concatenate percentage and material, convert material to lowercase
    result = [
        f"{percentage.replace(' ', '')} {material.lower()}"
        for percentage, material in matches
    ]

    return result
