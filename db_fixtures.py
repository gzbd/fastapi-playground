import os
import yaml
import glob
import functools
from typing import Any

from db import async_db


def load_all_fixture_files(dirpath: str) -> dict[str, list[dict]]:
    yamlfiles = glob.glob(os.path.join(dirpath, "*.yml"))
    fixtures = [load_fixture_file(fpath) for fpath in yamlfiles]
    return {tname: items for tname, items in fixtures}


def load_fixture_file(path: str) -> tuple[str, list[dict]]:
    tname = os.path.splitext(os.path.basename(path))[0]
    with open(path, "r") as fp:
        return tname, yaml.safe_load(fp)


def to_sql(tname: str, items: list[dict[Any, Any]]) -> str:
    def as_param(items: list[str]) -> list[str]:
        return [f":{item}" for item in items]

    return f"INSERT INTO {tname}({', '.join(items[0].keys())}) VALUES ({', '.join(as_param(items[0].keys()))});"


def fixtures(dirpath: str):
    def wrapper(func):
        async def wrapped(*args, **kwargs):
            fixtures = load_all_fixture_files(dirpath)
            for tname, items in fixtures.items():
                sql = to_sql(tname, items)
                await async_db.execute_many(query=sql, values=items)

            try:
                result = await func(*args, **kwargs)
            except AssertionError as ex:
                raise ex
            finally:
                for tname in fixtures.keys():
                    await async_db.execute(f"DELETE FROM {tname}")
            return result

        return wrapped

    return wrapper
