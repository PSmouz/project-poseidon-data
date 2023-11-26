import unittest
from poseidonscraper.utils import extract_materials


class ExtractMaterialsTest(unittest.TestCase):
    def test_extract_materials_single_material(self):
        value = "Material: 100% Cotton"
        expected_result = ["100% cotton"]
        result = extract_materials(value)
        self.assertEqual(result, expected_result)

    def test_extract_materials_multiple_materials(self):
        value = "Material: 54 % Polyamide, 39 % Polyester & 7 % Elasthan"
        expected_result = ["54% polyamide", "39% polyester", "7% elasthan"]
        result = extract_materials(value)
        self.assertEqual(result, expected_result)

    def test_extract_materials_german_und_keyword(self):
        value = "Material: 65 % Cotton und 35 % Polyester"
        expected_result = ["65% cotton", "35% polyester"]
        result = extract_materials(value)
        self.assertEqual(result, expected_result)


if __name__ == "__main__":
    unittest.main()
