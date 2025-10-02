# /// script
# dependencies = [
#   "duckdb",
#   "httpx",
# ]
# ///

import pathlib
import zipfile

import duckdb
import httpx


METHYLATION_PATH = pathlib.Path("methylation.zip")
EXPRESSION_PATH = pathlib.Path("expression.zip")

EXPRESSION_DB_URL = "https://oncodb.org/download/expression/expression.zip"
METHYLATION_DB_URL = "https://oncodb.org/download/methylation/methylation.zip"


def get_oncodb_data():
    if not METHYLATION_PATH.exists():
        with httpx.stream("GET", METHYLATION_DB_URL) as response:
            response.raise_for_status()
            with open(METHYLATION_PATH, "wb") as f:
                for chunk in response.iter_bytes():
                    f.write(chunk)

        with zipfile.ZipFile(METHYLATION_PATH, "r") as z:
            z.extractall()

    if not EXPRESSION_PATH.exists():
        with httpx.stream("GET", EXPRESSION_DB_URL) as response:
            response.raise_for_status()
            with open(EXPRESSION_PATH, "wb") as f:
                for chunk in response.iter_bytes():
                    f.write(chunk)

        with zipfile.ZipFile(EXPRESSION_PATH, "r") as z:
            z.extractall()


def query_expression():
    with duckdb.connect(":memory:") as conn:
        conn.sql("""
            SELECT
                "Gene Symbol" AS subject,
                CASE
                    WHEN "log2 fold change" > 0 THEN 'increased in'
                    WHEN "log2 fold change" < 0 THEN 'decreased in'
                    ELSE 'no change'
                END AS predicate,
                "Cancer type" AS object,
                "log2 fold change" AS change,
                "FDR adjusted p-value" AS p,
                split(filename, '_')[-2] AS data_type
            FROM read_csv("expression/*_Table.txt", types={'NCBI gene id': 'VARCHAR'}, union_by_name=True)
            WHERE "FDR adjusted p-value" < 0.05;
        """)


def query_methylation():
    with duckdb.connect(":memory:") as conn:
        conn.sql("""
            SELECT "Gene symbol" AS subject,
                    CASE
                        WHEN "log2 fold change" > 0 THEN 'increased in'
                        WHEN "log2 fold change" < 0 THEN 'decreased in'
                        ELSE 'no change'
                    END AS predicate,
                    "Cancer Type" AS object,
                    "FDR adjusted p-value",
                    "log2 fold change"
            FROM read_csv("expression/*_Table.txt", union_by_name=True)
            WHERE "FDR adjusted p-value" < 0.05;
        """)


def main():
    get_oncodb_data()
    # TODO: remap acronyms to disease ontology


if __name__ == "__main__":
    # uv run build_oncodb_triples.py
    main()
