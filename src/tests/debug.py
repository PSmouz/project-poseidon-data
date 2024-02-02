import re


def remove_span_tags(html_text):
    """Removes HTML span tags from a string.

    The opening and closing tags are removed separately to avoid overlapping
    tags. The text between the tags is preserved. The span tags can also
    have various attributes in the opening tag.

    Args:
        html_text: The HTML text to remove the <span> tags from.

    Returns:
        The HTML text with the <span> tags removed, but inner text
        preserved.
    """
    # Capture <span> tags, open and close separately to avoid overlapping
    # <span\s*.*?> because there can be attributes in the opening tag
    s = re.compile(r"<span\s*.*?>")
    s2 = re.compile(r"</span>")

    # Replace <span> tags with their inner text in the value
    text = re.sub(s, "", html_text)
    cleaned_text = re.sub(s2, "", text)
    return cleaned_text


if __name__ == "__main__":
    # print(["leggings", "underwear"].split(","))
    # data = ["Brown", "colors_digital-seamless-leggings", "Taupe_color"]
    # print(
    #     next(
    #         (item.split("_")[0].lower() for item in data if "_color" in item),
    #         None,
    #     )
    # )

    t = (
        "<b>Fabric Content: </b>Leotard: 82% Polyester / 18% Spandex | "
        "Straps: 80% Nylon / 20% Spandex<br><br>"
    )

    pattern = re.compile(
        r"(?P<percentage>\d{1,3}(?:\.\d{1,2})?(?:\s*|&nbsp;)%)(?:\s*|&nbsp;)"
        r"(?P<material>[\w\s]+?)(?=\s*,|\s*<|\s*(?:\d{1,3}\s?%|$|\s*[&.]|"
        r"\s*und|\s*\/|\s*\|))"
    )

    matches = pattern.findall(t)
    print(matches)
    # Concatenate percentage and material, convert material to lowercase
    result = [
        f"{percentage.replace(' ', '').strip()} {material.lower()}"
        for percentage, material in matches
    ]

    print(result)
