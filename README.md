# Variant_Drug_KG
Build a knowledge graph connecting variants, drugs, and clinical evidence to identify therapeutic opportunities (e.g. CIViC - Clinical Interpretations of Variants in Cancer)

Basing this on the Molecular Targets Project https://moleculartargets.ccdi.cancer.gov/  and the PMTL https://moleculartargets.ccdi.cancer.gov/fda-pmtl

Nodes: genes, diseases, drugs, pathway names etc.  Edges: relationships (with or w/out properties). 

Order of operations: Ingestion of GENCODE or HGNC, then CIVIC, then PMTL, then aggregated somatic variant data from Kids First/TARGET (as part of the molecular targets project, see above).  Also aggregated somatic variant data from TCGA if available (by cancer/cohort).

![FlowChart](Untitled-2025-10-01-1244.png)
