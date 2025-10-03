import pandas as pd
from typing import List, Optional
# Aim - Format files in consistent triple format

def formatting_triples(infile_path: str,
                       sep: str):
    """
    Here we are expecting a tsv/csv as input
    - Write separate node / relationship lists to file
    - Optional metadata additions
    """
    input_df = pd.read_csv(infile_path, sep=sep)
    print(input_df.columns)
    print(input_df)

    # Prepare drugs nodes (unique)
    drugs_df = input_df[['drug_id', 'drug_name', 'isApproved', 'hasBeenWithdrawn']].drop_duplicates()
    drugs_df.rename(columns={'drug_id': 'id', 'drug_name': 'name'}, inplace=True)
    
    # Prepare disease nodes (unique)
    diseases_df = input_df[['disease_id', 'disease']].drop_duplicates()
    diseases_df.rename(columns={'disease_id': 'id', 'disease': 'name'}, inplace=True)

    # Prepare relationships with features
    relationships_df = input_df[['drug_id', 'disease_id', 'maximumClinicalTrialPhase']].copy()
    relationships_df.rename(columns={'drug_id': 'subject',
                                     'disease_id': 'object',
                                     'maximumClinicalTrialPhase': 'maxClinicalTrialPhase'}, inplace=True)

    base_path = "/Users/withers/GitProjects/aws_hackathon/Variant_Drug_KG/data_processing/OTs_drugdis_data"
    # Write CSVs for bulk import into Neo4j
    drugs_df.to_csv(f"{base_path}/drugs.csv", index=False)
    diseases_df.to_csv(f"{base_path}/diseases.csv", index=False)
    relationships_df.to_csv(f"{base_path}/drug_disease_interactions.csv", index=False)

formatting_triples(infile_path="/Users/withers/GitProjects/aws_hackathon/ot_drug_indication.tsv", sep="\t")