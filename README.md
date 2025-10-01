# Variant_Drug_KG
Build a knowledge graph connecting variants, drugs, and clinical evidence to identify therapeutic opportunities (e.g. CIViC - Clinical Interpretations of Variants in Cancer)

Analysis target: Pediatric cancers, which have historically been underserved in terms of therapeutic development and clinical trials, as drug companies were not previously required to study pediatric cancers. Most pediatric therapeutic discovery is done by pediatrics researchers, not drug companies.    The FDA's Pediatric Molecular Target List is a list of genes that pediatric clinician experts have outlined as critical to address to treat pediatric cancer. The RACE for Children Act (USA, https://www.congress.gov/bill/115th-congress/house-bill/1231) recently made it a rule that if an actionable mutation or gene for an adult cancer is being targeted by pharma/biotech, and if that target is in the PMTL,then the company must justify why they are not testing it or they must trial the drug in children.

Basing this project therefore on pediatric cancers, where the data has been harmonized for the Molecular Targets Project (MTP: https://moleculartargets.ccdi.cancer.gov/)  and the FDA PMTL https://moleculartargets.ccdi.cancer.gov/fda-pmtl

The Molecular Targets Project's data was produced at the Children's Hospital of Philadelphia with aligned RNA and DNA sequence data by the Kids First Data Resource Center from Kids First, TARGET and other pediatric cancer datasets.  The data was all harmonized with the OpenPedCan  suite of tools https://github.com/d3b-center/OpenPedCan-analysis cited here: https://pubmed.ncbi.nlm.nih.gov/39026781/ and used in the MTP website.

Nodes for this KG: genes, diseases, drugs, pathway names etc.  Edges: relationships. 

Order of operations: Ingestion of GENCODE or HGNC, then CIVIC, then PMTL, then aggregated somatic variant data from Kids First/TARGET (as part of the molecular targets project, see above).  Also aggregated somatic variant data from TCGA if available (by cancer/cohort).

![FlowChart](Untitled-2025-10-01-1244.png)
