import pandas as pd
from typing import List, Optional
# Aim - Format files in consistent triple format

def formatting_triples(infile_path: str,
                       sep: str,
                       subject: str,
                       subject_meta: Optional[List] = None,
                       predicate: str,
                       predicate_meta: Optional[List] = None,
                       object: str,
                       object_meta: Optional[List] = None):
    """
    Here we are expecting a tsv/csv as input
    - Declare subject, predicate, object of input file
    - Write separate node / relationship lists to file
    - Optional metadata additions
    """
    input_df = pd.read_csv(infile_path, sep=sep)
    print(input_df.columns)
    print(input_df)

formatting_triples(infile_path="/Users/withers/GitProjects/aws_hackathon/ot_drug_indication.tsv",
                   sep="\t",
                   subject="drug_id",
                   subject_meta = []
                   predicate = " ",
                   predicate_meta = []
                   object = "disease_id"
                   object_meta = [])