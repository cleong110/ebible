import os
import sys
import unittest
from pathlib import Path

TESTS_DIR = Path(__file__).resolve().parent
CODE_DIR = TESTS_DIR.parent / "code" / "python"
sys.path.insert(0, str(CODE_DIR))

# settings_file reads vrs_diffs.yaml by relative path.
os.chdir(CODE_DIR)
from settings_file import get_book_names, get_corpus, get_versification, get_vrs_diffs

vrs_diffs = get_vrs_diffs()
os.chdir(TESTS_DIR)


class Test_Get_Versification(unittest.TestCase):

    def setUp(self):
        self.versifications = TESTS_DIR / "versifications"

    def test_lxx(self):
        versification = get_versification(
            self.versifications / "eng-lxx2012", vrs_diffs
        )
        self.assertEqual(versification, "Septuagint")

    def test_english_acts_19_41(self):
        # Acts 19 ending at verse 41 is unique to English versification.
        versification = get_versification(self.versifications / "eng-acts19", vrs_diffs)
        self.assertEqual(versification, "English")

    def test_corpus_is_read_from_numbered_book_files(self):
        # Every fixture uses eBible's numbered file names (e.g. 74-ACTeng-acts19.usfm).
        # Reading none of their verses means detection silently falls back to a
        # default, which is how every 2025 extract came to be read as "Original".
        for project in sorted(self.versifications.iterdir()):
            with self.subTest(project=project.name):
                lines = get_corpus(project, vrs_diffs)
                self.assertTrue(any(text for text, _, _ in lines))


class Test_Misc(unittest.TestCase):

    def test_get_book_names(self):
        book_names_path = TESTS_DIR / "book_names"
        aai_books = get_book_names(book_names_path / "aai")
        self.assertTupleEqual(aai_books[0], ("MAT", "46-MATaai.usfm"))
        ahr_books = get_book_names(book_names_path / "ahr-NTAii20-Ahirani-Devanagari")
        self.assertTupleEqual(ahr_books[0], ("MAT", "MAT.usfm"))
        am_books = get_book_names(book_names_path / "am_ulb")
        self.assertTupleEqual(am_books[0], ("GEN", "01-GEN.usfm"))


if __name__ == "__main__":
    unittest.main()
