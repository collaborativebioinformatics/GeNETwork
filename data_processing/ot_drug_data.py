import pandas as pd

def read_infile(file_path: str) -> pd.DataFrame:
    return pd.read_parquet(file_path)

def parse_drug_ind(input_df: pd.DataFrame) -> pd.DataFrame:
    """
    Triple format would be:
        DRUG -- TREATS --> DISEASE
        - id                indications
                                - for each indication
                                - efoName
                                - disease
                                - maxphase
    Return pd.DataFrame
    """
    results = []
    for i, row in input_df.iterrows():
        indications = row["indications"]
        for ind in indications:
            results.append({
                    "drug_id" : row["id"],
                    "disease": ind["efoName"],
                    "disease_id": ind["disease"],
                    }
            ) # TODO - Only other part to extract here would be reference data?

    return pd.DataFrame(results)

def try_catch(row, element):
    try:
        return row[element]["rows"]
    except:
        return []

def parse_drug_mol(input_df: pd.DataFrame) -> pd.DataFrame:
    results = []
    for i, row in input_df.iterrows():
        
        results.append({
                "drug_name" : row["name"],
                "drug_id": row["id"],
                "isApproved": row["isApproved"],
                "hasBeenWithdrawn": row["hasBeenWithdrawn"],
                "maximumClinicalTrialPhase": row["maximumClinicalTrialPhase"]
                }
        ) # TODO - Is this all the data we wish to extract?

    return pd.DataFrame(results)

def join_dataframes(df1: pd.DataFrame,
                    df2: pd.DataFrame,
                    merge_on_l: str,
                    merge_on_r: str) -> pd.DataFrame:

    merged_df = pd.merge(df1, df2, left_on = merge_on_l, right_on = merge_on_r, how="left", suffixes=('_left', '_right'))
    print(merged_df.columns)
    # Merge and clean up
    merged_df['drug_id'] = merged_df['drug_id'].fillna(merged_df['drug_id'])
    # merged_df = merged_df.drop(['drug_left', 'drug_right'], axis=1)
    merged_df = merged_df.drop_duplicates()
    merged_df = merged_df[["drug_id", "drug_name", "disease_id", "disease", "maximumClinicalTrialPhase", "isApproved", "hasBeenWithdrawn"]]

    return merged_df

if __name__ == "__main__":
    """
    (1.) Read-in download of OTs drug indication data
         - OTs data accessed at ftp://ftp.ebi.ac.uk/pub/databases/opentargets/platform/25.09/output/drug_indication
    (2.) Read-in download of OTs drug molecule data
         - OTs data accessed at ftp://ftp.ebi.ac.uk/pub/databases/opentargets/platform/25.09/output/drug_molecule
    (3.) Desired output: triple format suitable for KG ingestion
    """

    drugind_path = "drug_indication/part-00000-0e2ed002-bc1a-4c53-855e-822517b3bdf3-c000.snappy.parquet"
    drug_indication = read_infile(file_path = drugind_path)
    drug_indication_df = parse_drug_ind(input_df = drug_indication)
    print(drug_indication_df.columns)
    
    drugmol_path = "drug_molecule/part-00000-35323264-2241-4256-b643-3a92cd0230e5-c000.snappy.parquet"
    drug_molecule = read_infile(file_path = drugmol_path)
    drug_molecule_df = parse_drug_mol(input_df = drug_molecule)
    print(drug_molecule_df.columns)

    # Here, tie together the two dataframes, finalising triples of DRUG -- TARGETS -- DISEASE, with
    # associated metadata
    merged_df = join_dataframes(drug_indication_df, drug_molecule_df, merge_on_l= "drug_id", merge_on_r="drug_id")
    print(merged_df)
    merged_df.to_csv("./ot_drug_indication.tsv", sep="\t")