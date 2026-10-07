import unittest

from validation.compare_metadata import (
    STATUS_MATCH,
    STATUS_MISMATCH,
    STATUS_MISSING,
    compare_record,
)


class CompareTests(unittest.TestCase):
    def setUp(self):
        self.rules = {"project_number": {"strip_prefixes": ["NRF", "MSIT"]}}
        self.authority = {"research inst. a": "Research Institute A"}

    def test_expected_match(self):
        master = {
            "paper_id": "P1",
            "title": "A Study",
            "journal": "Demo Journal",
            "oa": "Y",
            "project_numbers": "2026-001",
            "affiliations": "Research Institute A",
            "author_count": 1,
        }
        extracted = {
            "paper_id": "P1",
            "title": "A Study",
            "journal": "Demo Journal",
            "open_access": "Y",
            "project_numbers": ["NRF-2026-001"],
            "authors": [
                {"name": "A", "role": "first", "affiliations": ["Research Inst. A"]}
            ],
        }
        rows = compare_record(master, extracted, self.rules, self.authority)
        self.assertTrue(all(row["status"] == STATUS_MATCH for row in rows))

    def test_missing_oa_and_project_mismatch(self):
        master = {
            "paper_id": "P2",
            "title": "A Study",
            "journal": "Demo Journal",
            "oa": None,
            "project_numbers": "PRJ-1",
            "affiliations": "Institute A",
            "author_count": 1,
        }
        extracted = {
            "paper_id": "P2",
            "title": "A Study",
            "journal": "Demo Journal",
            "open_access": "Y",
            "project_numbers": ["PRJ-2"],
            "authors": [
                {"name": "A", "role": "first", "affiliations": ["Institute A"]}
            ],
        }
        rows = compare_record(master, extracted, self.rules, {})
        status_by_field = {row["field"]: row["status"] for row in rows}
        self.assertEqual(status_by_field["oa"], STATUS_MISSING)
        self.assertEqual(status_by_field["project_numbers"], STATUS_MISMATCH)


if __name__ == "__main__":
    unittest.main()
