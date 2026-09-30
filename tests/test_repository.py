import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]

class RepositoryFoundationTests(unittest.TestCase):
    def test_required_top_level_boundaries_exist(self):
        required = ["apps", "packages", "services", "api", "db", "schemas", "tests", "docs", "config", "scripts"]
        for path in required:
            self.assertTrue((ROOT / path).is_dir(), path)

    def test_readme_exists(self):
        self.assertTrue((ROOT / "README.md").is_file())

if __name__ == "__main__":
    unittest.main()
