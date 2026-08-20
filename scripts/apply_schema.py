from __future__ import annotations

import os
import subprocess
import sys

import ydb


def _statements(path: str) -> list[str]:
    with open(path, encoding="utf-8") as f:
        raw = f.read()
    without_comments = "\n".join(line for line in raw.splitlines() if not line.strip().startswith("--"))
    return [stmt.strip() for stmt in without_comments.split(";") if stmt.strip()]


def _iam_token() -> str:
    result = subprocess.run(["yc", "iam", "create-token"], capture_output=True, text=True, check=True)
    return result.stdout.strip()


def main() -> None:
    schema_path = sys.argv[1] if len(sys.argv) > 1 else "src/ydb_tickets/schema.sql"
    endpoint = os.environ["YDB_ENDPOINT"]
    database = os.environ["YDB_DATABASE"]

    driver = ydb.Driver(endpoint=endpoint, database=database, credentials=ydb.AccessTokenCredentials(_iam_token()))
    driver.wait(fail_fast=True, timeout=30)

    with ydb.SessionPool(driver, size=1) as pool:
        for statement in _statements(schema_path):
            print(f"--- applying ---\n{statement}\n")
            pool.retry_operation_sync(lambda session, query=statement: session.execute_scheme(query))

    print("schema applied")


if __name__ == "__main__":
    main()
