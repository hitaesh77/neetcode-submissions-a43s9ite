import sys
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
from refresh_metadata import parse_catalog


class MetadataTests(unittest.TestCase):
    def test_neetcode_id_maps_different_leetcode_slug(self):
        catalog = parse_catalog('{problem:"Two Sum",pattern:"Arrays & Hashing",'
                                'link:"two-sum/",difficulty:"Easy",ncLink:"two-integer-sum/"}')
        entry = catalog["two-integer-sum"]
        self.assertEqual(entry["difficulty"], "Easy")
        self.assertEqual(entry["links"]["leetcode"], "https://leetcode.com/problems/two-sum/")
        self.assertEqual(entry["topics"], ["Arrays & Hashing"])

    def test_no_neetcode_link_uses_catalog_slug(self):
        catalog = parse_catalog('{problem:"Example",pattern:"JavaScript",'
                                'link:"example/",difficulty:"Medium"}')
        self.assertNotIn("neetcode", catalog["example"]["links"])

    def test_invalid_or_changed_catalog_fails(self):
        for text in ('no catalog', '{problem:"Example",link:"example/"}',
                     '{problem:"Example",pattern:"Stack",link:"example/",difficulty:"Impossible"}'):
            with self.subTest(text=text), self.assertRaises(ValueError):
                parse_catalog(text)

    def test_duplicate_ids_fail(self):
        row = '{problem:"Example",pattern:"Stack",link:"example/",difficulty:"Hard"}'
        with self.assertRaisesRegex(ValueError, "Duplicate"):
            parse_catalog(row + ',' + row)
