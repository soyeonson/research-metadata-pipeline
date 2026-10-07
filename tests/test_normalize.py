import unittest

from validation.normalize import (
    normalize_affiliation,
    normalize_oa,
    normalize_project_number,
)


class NormalizeTests(unittest.TestCase):
    def test_project_number_prefix_and_dash(self):
        self.assertEqual(
            normalize_project_number("NRF – 2026-R1A1-001", ["NRF"]),
            "2026-R1A1-001",
        )

    def test_oa(self):
        self.assertEqual(normalize_oa("open access"), "Y")
        self.assertIsNone(normalize_oa(""))

    def test_affiliation_authority(self):
        mapping = {"research inst. a": "Research Institute A"}
        self.assertEqual(
            normalize_affiliation("Research Inst. A", mapping),
            "Research Institute A",
        )


if __name__ == "__main__":
    unittest.main()
