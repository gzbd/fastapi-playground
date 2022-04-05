import unittest
import tempfile
import os
import yaml

from .db_fixtures import load_fixture_file, load_all_fixture_files, to_sql


class TestLoadFixtureFile(unittest.TestCase):
    def test_ok(self):
        content = """
        - column1: value1
          column2: value2
        """
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yml") as fp:
            fp.write(content)
            fp.flush()

            tname, items = load_fixture_file(fp.name)

            wantName = _get_tmp_fname(fp.name)
            self.assertEqual(tname, wantName)
            self.assertEqual(items, [{"column1": "value1", "column2": "value2"}])

    def test_bad_yml(self):
        content = """
        - column1: value1
            column2: value2
        """
        with tempfile.NamedTemporaryFile(mode="w", suffix=".yml") as fp:
            fp.write(content)
            fp.flush()

            self.assertRaises(yaml.YAMLError, load_fixture_file, fp.name)


class TestLoadAllFixtureFiles(unittest.TestCase):
    def test_ok(self):
        content = """
        - column1: value1
          column2: value2
        """
        with (
            tempfile.NamedTemporaryFile(mode="w", suffix=".yml") as fp1,
            tempfile.NamedTemporaryFile(mode="w", suffix=".yml") as fp2,
        ):
            fp1.write(content)
            fp1.flush()
            fp2.write(content)
            fp2.flush()

            fixtures = load_all_fixture_files(tempfile.gettempdir())

            self.assertEqual(
                fixtures,
                {
                    _get_tmp_fname(fp1.name): [
                        {"column1": "value1", "column2": "value2"}
                    ],
                    _get_tmp_fname(fp2.name): [
                        {"column1": "value1", "column2": "value2"}
                    ],
                },
            )


def _get_tmp_fname(path: str) -> str:
    return os.path.splitext(os.path.basename(path))[0]


class TestToSQL(unittest.TestCase):
    def test_ok(self):
        sql = to_sql("table1", [{"column1": "value1", "column2": "value2"}])
        self.assertEqual(
            sql, "INSERT INTO table1(column1, column2) VALUES (:column1, :column2);"
        )
