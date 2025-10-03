# /// script
# dependencies = [
#   "duckdb",
#   "httpx",
# ]
# ///

import pathlib
import shutil
import os
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


def oncodb_disease_mapping(conn):
    conn.sql("""
        CREATE OR REPLACE TABLE disease_mapping AS
                SELECT * FROM read_csv('doid_codes.csv');
    """)


def load_expression(conn):
    conn.sql("""
        CREATE OR REPLACE VIEW expression_view AS
        WITH filtered AS (
            SELECT
                "Gene Symbol" AS subject,
                CASE
                    WHEN "log2 fold change" > 0 THEN 'increased in'
                    WHEN "log2 fold change" < 0 THEN 'decreased in'
                    ELSE 'no change'
                END AS predicate,
                "Cancer type"          AS cancer_type,
                "log2 fold change"     AS change,
                "FDR adjusted p-value" AS p,
                'Expression'           AS data_type
            FROM read_csv(
                'expression/*_Table.txt',
                types = {'NCBI gene id': 'VARCHAR'},
                union_by_name = TRUE
            )
            WHERE "FDR adjusted p-value" < 0.05
        )
        SELECT
            f.subject,
            f.predicate,
            d.efoid AS object,
            f.data_type,
            f.p,
            f.change
        FROM filtered f
        JOIN disease_mapping d
        ON f.cancer_type = d.oncodb;
    """)


def load_methylation(conn):
    conn.sql("""
        CREATE OR REPLACE VIEW methylation_view AS
        WITH filtered AS (
            SELECT
                "Gene symbol"          AS subject,
                'associated with'      AS predicate,
                "Cancer Type"          AS cancer_type,
                "FDR adjusted p-value" AS p,
                "Beta difference value" AS beta_diff,
                'Methylation'          AS data_type
            FROM read_csv('methylation/*_All_Table.txt', union_by_name = TRUE)
            WHERE "FDR adjusted p-value" < 0.05
        )
        SELECT
            f.subject,
            f.predicate,
            d.efoid AS object,
            f.data_type,
            f.p,
            f.beta_diff
        FROM filtered f
        JOIN disease_mapping d
        ON f.cancer_type = d.oncodb;
    """)


def write_nodes(conn):
    conn.sql("""
        CREATE OR REPLACE TABLE nodes AS
        -- start by concatenating all the rows
        WITH all_data AS (
            SELECT *
            FROM expression_view
            UNION ALL
            SELECT *
            FROM methylation_view
        ),
        -- get node names
        nodes AS (
            SELECT subject AS name, 'Gene' AS label
            FROM all_data
            UNION
            SELECT object AS name, 'Disease' AS label
            FROM all_data
        )
        -- create node ids
        SELECT
            row_number() OVER (ORDER BY name) AS id,
            name,
            label
        FROM nodes;
    """)
    # make sure each node is unique
    conn.sql("ALTER TABLE nodes ADD PRIMARY KEY (name)")
    conn.sql("SELECT * FROM nodes").write_csv(
        "nodes", partition_by=["label"], overwrite=True
    )


def write_edges(conn):
    conn.sql("""
    CREATE OR REPLACE TABLE edges AS (
        WITH all_data AS (
            SELECT *
            FROM expression_view
            UNION ALL
            SELECT *
            FROM methylation_view
        )
        SELECT
             subject AS "from",
             object AS "to",
             "data_type",
             p,
             change
        FROM all_data
    );
    """)
    conn.sql("SELECT * FROM edges").write_csv("edges.csv")


def zip_output():
    # make a zip of the 'nodes' directory
    shutil.make_archive("oncodb", "zip", root_dir="nodes")

    # add 'edges.csv' to the existing zip
    with zipfile.ZipFile("oncodb.zip", "a", zipfile.ZIP_DEFLATED) as zipf:
        zipf.write("edges.csv", os.path.basename("edges.csv"))


def main():
    get_oncodb_data()

    with duckdb.connect("oncodb.duckdb") as duckdb_conn:
        oncodb_disease_mapping(duckdb_conn)
        load_expression(duckdb_conn)
        load_methylation(duckdb_conn)
        write_nodes(duckdb_conn)
        write_edges(duckdb_conn)
        zip_output()


if __name__ == "__main__":
    # uv run build_oncodb_triples.py
    main()
