import json
import tempfile
import unittest
from pathlib import Path

from processing.transient_processor import process_file
from storage.result_store import save_derived_json


class TransientProcessingTests(unittest.TestCase):
    def test_payload_has_no_source_text(self):
        sample = Path("samples/synthetic_article.txt")
        payload = process_file(sample, "PAPER_SYNTHETIC")
        serialized = json.dumps(payload, ensure_ascii=False)

        self.assertNotIn("SYNTHETIC ARTICLE FIXTURE", serialized)
        self.assertNotIn("Acknowledgements\nThis synthetic work", serialized)
        self.assertEqual(
            payload["papers"][0]["provenance"]["persistence_policy"],
            "derived_metadata_only",
        )
        self.assertTrue(payload["papers"][0]["provenance"]["source_hash"])
        self.assertEqual(payload["papers"][0]["authors"][0]["name"], "Alice Kim")

    def test_store_rejects_source_content_field(self):
        payload = {"papers": [{"paper_id": "P1", "source_text": "do not persist"}]}
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(ValueError):
                save_derived_json(payload, Path(tmp) / "out.json")

    def test_store_rejects_abstract_and_raw_response(self):
        for forbidden_key in ("abstract", "raw_response"):
            payload = {"papers": [{"paper_id": "P1", forbidden_key: "do not persist"}]}
            with tempfile.TemporaryDirectory() as tmp:
                with self.assertRaises(ValueError):
                    save_derived_json(payload, Path(tmp) / "out.json")


if __name__ == "__main__":
    unittest.main()
