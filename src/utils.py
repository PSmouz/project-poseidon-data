import re

from bs4 import BeautifulSoup


# from w3lib.html import remove_tags


def extract_materials(html_text):
    """
    Passes tests for:
     - Teveo

    Args:
        html_text:

    Returns:

    """

    def remove_tags(html_text):
        """
        Removes HTML tags from a string.
        Args:
            html_text:

        Returns:

        """
        soup = BeautifulSoup(html_text.replace("\\", ""), "html.parser")
        return soup.get_text(separator=" ", strip=True)

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

    def materials_sum_up_to_100(materials: list) -> list:
        """Makes sure that the sum of the percentages is 100.

        If the sum is greater than 100, the function returns the first
        materials that sum up to 100. If the sum is less than 100, the
        function returns the materials as they are. (This is especially used
        with the GKElite leotard materials, where the sum is greater than 100
        as they differ between leotard and straps for example.)


        Args:
            materials: The list of materials with percentages e.g. ["82%
            Polyester", "18% Spandex"]

        Returns: The first k materials that sum up to 100.

        """
        sum_percentage = 0.0
        out = []
        for material in materials:
            percentage = float(material.split("%")[0])
            sum_percentage += percentage
            if sum_percentage > 100.0:
                break
            out.append(material)
            if sum_percentage == 100.0:
                break
        return out

    # Regex pattern to match percentage and material
    pattern = re.compile(
        r"(?P<percentage>\d{1,3}(?:\.\d{1,2})?(?:\s*|&nbsp;)%)(?:\s*|&nbsp;)"
        r"(?P<material>[\w\s]+?)(?=\s*,|\s*<|\s*(?:\d{1,3}\s?%|$|\s*[&.]|"
        r"\s*und|\s*\/|\s*\|))"
    )

    # Needed because backslashes create problems for tag removal.
    text = html_text.replace("\\", "")
    # Remove HTML tags from the value
    clean_text = remove_span_tags(text)
    # Extract matches from the value
    matches = pattern.findall(clean_text)
    # Concatenate percentage and material, convert material to lowercase
    result = [
        f"{percentage.replace(' ', '').strip()} {material.lower()}"
        for percentage, material in matches
    ]

    return materials_sum_up_to_100(result)


def parse_css_colors(css):
    """
    Parses a CSS file and returns a dictionary of selectors and colors.

    Args:
        css:

    Returns:

    """
    pattern = (
        r"\.([\w-]+)(?:,\s*([\w-]+))?\s*{\s*background-color\s*:\s*#(["
        r"0-9a-fA-F]+)(?:\s*;\s*)?}"
    )
    # Find all matches using the pattern
    matches = re.findall(pattern, css)
    # Create a dictionary to store the parsed data
    parsed_data = {}
    # Process each match and populate the dictionary
    for match in matches:
        selector1, selector2, background_color = match
        selector1 = selector1.strip()
        selector2 = selector2.strip() if selector2 else None
        background_color = background_color.strip()

        # Handle multiple selectors
        if selector2:
            selectors = [selector1, selector2]
        else:
            selectors = [selector1]

        for selector in selectors:
            # Update the parsed_data dictionary
            parsed_data[selector] = "#" + background_color

    return parsed_data


color_map = {
    "oa-product-color--zebra-smokey-rose": "#c18080",
    "oa-product-color--zebra-purple": "#b5b1e5",
    "oa-product-color--zebra-power-pink": "#dd0585",
    "oa-product-color--zebra-off-white": "#fcf5e3",
    "oa-product-color--zebra-black": "#000000",
    "oa-product-color--wood-rose": "#B57272",
    "oa-product-color--winter-blush": "#f88180",
    "oa-product-color--wine": "#6b2c5f",
    "oa-product-color--white-rose-purple": "#b5b1e5",
    "oa-product-color--white-multicolor": "#ffffff",
    "oa-product-color--white": "#ffffff",
    "oa-product-color--venice-blue": "#789dde",
    "oa-product-color--velvet-rose": "#7e374e",
    "oa-product-color--velvet-powder": "#8e8e8e",
    "oa-product-color--velvet-plum": "#896e8b",
    "oa-product-color--velvet-black": "#000000",
    "oa-product-color--ultra-violet": "#7d6baf",
    "oa-product-color--turkis": "#02b0c8",
    "oa-product-color--transparent-poppy-orange": "#ff8a73",
    "oa-product-color--toffee-tan": "#7a6862",
    "oa-product-color--taupe-nude": "#927f7c",
    "oa-product-color--taupe-brown": "#644139",
    "oa-product-color--sweet-berry": "#cc5c7e",
    "oa-product-color--sunset-pink": "#e96393",
    "oa-product-color--sunflower-yellow": "#f99108",
    "oa-product-color--sun-yellow": "#fff800",
    "oa-product-color--summer-berry": "#d3075a",
    "oa-product-color--stormy-blue": "#465966",
    "oa-product-color--stone": "#d5c7bc",
    "oa-product-color--steel-grey-tie-dye": "#a4a8ab",
    "oa-product-color--steel-grey": "#8e8e8e",
    "oa-product-color--spearmint": "#7d9e89",
    "oa-product-color--soft-white": "#f4eee8",
    "oa-product-color--soft-sky-blue-tie-dye": "#9cc6f7",
    "oa-product-color--soft-palm-green": "#485e5a",
    "oa-product-color--soft-khaki": "#8a9678",
    "oa-product-color--soft-jade": "#8eb2a9",
    "oa-product-color--soft-camel": "#c6ac9b",
    "oa-product-color--soft-blush": "#ce97b4",
    "oa-product-color--soft-blue": "#5a6b72",
    "oa-product-color--soft-berry": "#cc7196",
    "oa-product-color--smokey-rose-lurex": "#c18090",
    "oa-product-color--smokey-rose": "#c18090",
    "oa-product-color--sky-blue": "#66acdd",
    "oa-product-color--skin": "#fad4d4",
    "oa-product-color--shiny-stone": "#d5c7bc",
    "oa-product-color--shiny-soft-blue": "#5a6b72",
    "oa-product-color--shiny-sand": "#ccac92",
    "oa-product-color--shiny-rose-gold": "#e8b1b1",
    "oa-product-color--shiny-red": "#c4060a",
    "oa-product-color--shiny-pink": "#ff50b8",
    "oa-product-color--shiny-petrol": "#00345e",
    "oa-product-color--shiny-khaki": "#404c39",
    "oa-product-color--shiny-deep-green": "#044042",
    "oa-product-color--shiny-cranberry": "#911445",
    "oa-product-color--shiny-cliff-grey": "#514a4e",
    "oa-product-color--shiny-blue": "#37378c",
    "oa-product-color--shiny-black": "#000000",
    "oa-product-color--shiny-atlantic-blue": "#2c3958",
    "oa-product-color--scarlet-red": "#f23041",
    "oa-product-color--sand": "#ccac92",
    "oa-product-color--rose-white": "#ebc8b2",
    "oa-product-color--rose-red": "#d01c1f",
    "oa-product-color--rose-quartz": "#f7cac9",
    "oa-product-color--rose-melange": "#e8b1b1",
    "oa-product-color--rose-gold": "#d99899",
    "oa-product-color--rose": "#e8b1b1",
    "oa-product-color--rock-crystal": "#8e8e8e",
    "oa-product-color--red": "#ff0800",
    "oa-product-color--purple-melange": "#b5b1e5",
    "oa-product-color--purple": "#b5b1e5",
    "oa-product-color--prism-pink": "#ed748b",
    "oa-product-color--power-pink": "#dd0585",
    "oa-product-color--power-blue": "#37378c",
    "oa-product-color--powder": "#8e8e8e",
    "oa-product-color--poppy-orange-tie-dye": "#fc9a8d",
    "oa-product-color--poppy-orange": "#ff8a73",
    "oa-product-color--petrol": "#00345e",
    "oa-product-color--peach-blush": "#ff9fa8",
    "oa-product-color--pastel-yellow": "#f5eabc",
    "oa-product-color--pastel-green": "#d1e7c8",
    "oa-product-color--paris-pink": "#d32e5e",
    "oa-product-color--papaya-orange": "#f9572b",
    "oa-product-color--palm-green": "#2e4c48",
    "oa-product-color--pale-soft-jade": "#e4f6e4",
    "oa-product-color--pale-rose": "#e9c9d1",
    "oa-product-color--pale-purple": "#cec1e0",
    "oa-product-color--pale-prism-pink": "#ff908d",
    "oa-product-color--pale-poppy-orange-tie-dye": "#ff9fa8",
    "oa-product-color--pale-poppy-orange": "#ff9fa8",
    "oa-product-color--pale-olive": "#697c6a",
    "oa-product-color--pale-jade": "#9ab7b0",
    "oa-product-color--orchid": "#c59ec6",
    "oa-product-color--orange-tie-dye": "#ff8a73",
    "oa-product-color--orange-multi": "#ff8a73",
    "oa-product-color--off-white-zebra": "#2e4c48",
    "oa-product-color--off-white": "#faf9f6",
    "oa-product-color--oceans-blue": "#2d2d7a",
    "oa-product-color--ocean-blue": "#6e7e99",
    "oa-product-color--nude": "#ebc8b2",
    "oa-product-color--none": "#ffffff",
    "oa-product-color--neon-yellow": "#f4ff0b",
    "oa-product-color--neon-pink-tie-dye": "#ffb3f6",
    "oa-product-color--neon-pink": "#ff69db",
    "oa-product-color--navy": "#2a3244",
    "oa-product-color--multicolor": "#ffffff",
    "oa-product-color--multi": "#ffffff",
    "oa-product-color--mint-tie-dye": "#b6dfc4",
    "oa-product-color--macchiato": "#aa8977",
    "oa-product-color--lurex-light-jade": "#b6dfc4",
    "oa-product-color--lurex-light-blue": "#a8d8ef",
    "oa-product-color--lime": "#dfef87",
    "oa-product-color--light-summer-berry": "#f185b5",
    "oa-product-color--light-rose": "#ffdbea",
    "oa-product-color--light-prism-pink": "#ffc7c7",
    "oa-product-color--light-nude": "#efe1ca",
    "oa-product-color--light-jade": "#b6dfc4",
    "oa-product-color--light-island-green": "#75c59a",
    "oa-product-color--light-grey-melange": "#e8e8ed",
    "oa-product-color--light-blue-gardient": "#98bcfa",
    "oa-product-color--light-blue": "#a8d8ef",
    "oa-product-color--leo": "#d1a68c",
    "oa-product-color--khaki": "#404c39",
    "oa-product-color--ivory": "#e9d7c7",
    "oa-product-color--island-green": "#008658",
    "oa-product-color--iced-mint": "#a4f0d8",
    "oa-product-color--grey-melange": "#a7a7aa",
    "oa-product-color--grey": "#8e8e8e",
    "oa-product-color--green-leo-print": "#514f3a",
    "oa-product-color--earth-brown": "#927f7c",
    "oa-product-color--dusty-rose": "#c18080",
    "oa-product-color--dusty-lilac": "#98858d",
    "oa-product-color--dove-blue": "#a1bce2",
    "oa-product-color--deep-green": "#044042",
    "oa-product-color--dazzling-blue": "#2e4da7",
    "oa-product-color--dark-wood-rose": "#7d4d55",
    "oa-product-color--dark-purple": "#39075f",
    "oa-product-color--dark-pink": "#921353",
    "oa-product-color--dark-navy": "#2a3244",
    "oa-product-color--dark-green": "#044042",
    "oa-product-color--dark-dove-blue": "#717388",
    "oa-product-color--dark-camel": "#c19a6b",
    "oa-product-color--dark-anthracite": "#3a363a",
    "oa-product-color--cranberry": "#911445",
    "oa-product-color--coral": "#ff7878",
    "oa-product-color--cool-berry": "#84555d",
    "oa-product-color--cloud-blue": "#b1ccdc",
    "oa-product-color--cliff-grey": "#514a4e",
    "oa-product-color--cherry-chocolate": "#602830",
    "oa-product-color--cha-cha-blush": "#f29b9b",
    "oa-product-color--caramel-brown": "#85461e",
    "oa-product-color--bubblegum": "#e46c99",
    "oa-product-color--brown-leo-print": "#644139",
    "oa-product-color--brown": "#8b4f39",
    "oa-product-color--bright-pink": "#dd0585",
    "oa-product-color--bright-berry": "#871659",
    "oa-product-color--boho-berry": "#854c65",
    "oa-product-color--blush": "#a0657d",
    "oa-product-color--blue": "#2d2d7a",
    "oa-product-color--black-white": "#000000",
    "oa-product-color--black-lurex": "#000000",
    "oa-product-color--black": "#000000",
    "oa-product-color--beige": "#e2cfb5",
    "oa-product-color--beach-dye": "#ffcfd3",
    "oa-product-color--bay-blue": "#58c9d4",
    "oa-product-color--baia-blue": "#71b5ab",
    "oa-product-color--azure-blue": "#004c8e",
    "oa-product-color--aubergine": "#4e3c5b",
    "oa-product-color--atlantic-blue": "#2c3958",
    "oa-product-color--aqua-haze": "#82b8bb",
    "oa-product-color--aqua-gray": "#a2b0a8",
    "oa-product-color--aqua": "#56d6ac",
    "oa-product-color--amethyst": "#885e95",
    "oa-product-color--amber-brown": "#9b391f",
    "oa-product-color--stormy-blue-tie-dye": "#465966",
    "oa-product-color--taupe-nude-tie-dye": "#927f7c",
    "oa-product-color--rose-tie-dye": "#e8b1b1",
    "oa-product-color--multi-pink": "#f7afad",
    "oa-product-color--multi-green": "#9ebab9",
    "oa-product-color--dolphin-blue": "#bbcbd3",
    "oa-product-color--70s-multi": "#df1e22",
    "oa-product-color--plum": "#720831",
    "oa-product-color--smokey-green": "#8f9991",
    "oa-product-color--moss": "#343f35",
    "oa-product-color--rose-water": "#ccae9e",
    "oa-product-color--yellow-stone": "#f4e398",
    "oa-product-color--cool-violet": "#6667ab",
    "oa-product-color--dark-chocolate": "#40312f",
    "oa-product-color--light-beige": "#c5bbae",
    "oa-product-color--sunny-peach": "#f4a6a3",
    "oa-product-color--winter-stone": "#c8c1b5",
    "oa-product-color--light-stone": "#e4e1d1",
    "oa-product-color--cinnamon": "#933c1d",
    "oa-product-color--light-orchid": "#c6b0d5",
    "oa-product-color--smaragd-green": "#375951",
    "oa-product-color--frosted-lavender": "#bdabbe",
    "oa-product-color--iris-pink": "#c07eb3",
    "oa-product-color--fire-orange": "#f5412a",
    "oa-product-color--grey-marble": "#c6c6c6",
    "oa-product-color--red-mahagony": "#6b4a4d",
    "oa-product-color--soft-grey": "#706f6f",
    "oa-product-color--wild-berry": "#ba6184",
    "oa-product-color--oatmeal": "#c8c0b7",
    "oa-product-color--fuchsia-pink": "#d40064",
    "oa-product-color--deep-sea-blue": "#1e1b49",
    "oa-product-color--deep-purple": "#4c2978",
    "oa-product-color--cyan": "#31b2b6",
    "oa-product-color--black-multi": "#000000",
    "oa-product-color--soft-cyan-melange": "#8dcde8",
    "oa-product-color--soft-purple-melange": "#d6abd2",
    "oa-product-color--soft-orange-melange": "#ee998d",
    "oa-product-color--oat-milk": "#e8e6d9",
    "oa-product-color--grey-lilac": "#696671",
    "oa-product-color--light-black": "#2d2d2d",
    "oa-product-color--grey-mauve": "#655e70",
    "oa-product-color--oak": "#e8e6d9",
    "oa-product-color--diva-pink": "#f4a6da",
    "oa-product-color--hazy-blue": "#8ccfea",
    "oa-product-color--limona": "#f6ff9f",
    "oa-product-color--limon": "#f6ff9f",
    "oa-product-color--light-grey-mauve": "#9590a0",
    "oa-product-color--california-rose": "#f4dce8",
    "oa-product-color--hot-pink": "#ed7eb3",
    "oa-product-color--soft-tropical-orange": "#f9b795",
    "oa-product-color--light-hazy-blue": "#95d8ef",
    "oa-product-color--light-hot-pink": "#f28fc1",
    "oa-product-color--light-tropical-orange": "#ffd2c0",
    "oa-product-color--sage-green": "#afbfa7",
    "oa-product-color--ultra-blue": "#1c3a77",
    "oa-product-color--soft-diva-pink": "#f2cce9",
    "oa-product-color--soft-oak": "#f9f7ef",
    "oa-product-color--soft-sage-green": "#c1ceba",
    "oa-product-color--soft-bay-blue": "#95b9e5",
    "oa-product-color--tropical-orange": "#fc8359",
    "oa-product-color--bold-hot-pink": "#ed3b90",
    "oa-product-color--dark-oak": "#4e4139",
    "oa-product-color--blue-moon": "#343646",
    "oa-product-color--deep-magenta": "#aa0746",
    "oa-product-color--marine-blue": "#2a3244",
    "oa-product-color--black-swirl": "#27272a",
    "oa-product-color--deep-plum": "#912a46",
    "oa-product-color--bold-hot-pink-swirl": "#ed3b90",
    "oa-product-color--burnt-orange": "#ae472d",
    "oa-product-color--ice-blue-swirl": "#c3e0f4",
    "oa-product-color--teal": "#254963",
    "oa-product-color--mellow-peach-swirl": "#dc7f64",
    "oa-product-color--snow-white": "#e3e3e3",
    "oa-product-color--forest-green": "#46483d",
    "oa-product-color--misty-lavender": "#be9cc1",
    "oa-product-color--shadow-lilac": "#4c2940",
    "oa-product-color--deep-pine-green": "#4a4f3a",
    "oa-product-color--tan": "#b4a899",
    "oa-product-color--matcha-green": "#c7dd83",
    "oa-product-color--iron-grey": "#98979a",
    "oa-product-color--moon-blue": "#343646",
    "oa-product-color--glacial-blue": "#92b5cb",
    "oa-product-color--crystal-white": "#f8faff",
    "oa-product-color--deep-teal": "#243d51",
    "oa-product-color--misty-lavender-swirl": "#be9cc1",
    "oa-product-color--glacial-blue-swirl": "#92b5cb",
    "oa-product-color--natural-cream": "#dad4c8",
    "oa-product-color--plain-black": "#27272a",
    "oa-product-color--vivid-green": "#009b75",
    "oa-product-color--autumn-rose": "#f5b0bd",
    "oa-product-color--rose-violet": "#c14189",
    "oa-product-color--candy-red": "#b20f2e",
}


class Node:
    """Implementation of a Node for a hashtable.

    Attributes:
        key: The key of the node.
        value: The value of the node.
        next: The next node in the linked list.

    """

    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None


class HashTable:
    """Implementation of a hashtable.

    Attributes:
        capacity: The capacity of the hashtable/number of buckets.
        size: The size of the hashtable.
        table: The table of the hashtable.
    """

    def __init__(self, capacity):
        self.capacity = capacity
        self.size = 0
        self.table = [None] * capacity

    def _hash(self, key):
        return hash(key) % self.capacity

    def insert(self, key, value):
        """Inserts a key-value pair into the hashtable.

        Args:
            key: The key of the key-value pair.
            value: The value of the key-value pair.

        """
        index = self._hash(key)

        if self.table[index] is None:
            self.table[index] = Node(key, value)
            self.size += 1
        else:
            current = self.table[index]
            while current:
                if current.key == key:
                    current.value = value
                    return
                current = current.next
            new_node = Node(key, value)
            new_node.next = self.table[index]
            self.table[index] = new_node
            self.size += 1

    def search(self, key):
        """Searches for a key in the hashtable.

        Args:
            key: The key to search for.

        Returns:
            The value of the key-value pair.
        """
        index = self._hash(key)

        current = self.table[index]
        while current:
            if current.key == key:
                return current.value
            current = current.next

        raise KeyError(key)

    def remove(self, key):
        """Removes a key-value pair from the hashtable.

        Args:
            key: The key of the key-value pair to remove.

        Returns:
            The value of the removed key-value pair.
        """
        index = self._hash(key)

        previous = None
        current = self.table[index]

        while current:
            if current.key == key:
                if previous:
                    previous.next = current.next
                else:
                    self.table[index] = current.next
                self.size -= 1
                return
            previous = current
            current = current.next

        raise KeyError(key)

    def __len__(self):
        return self.size

    def __contains__(self, key):
        try:
            self.search(key)
            return True
        except KeyError:
            return False
