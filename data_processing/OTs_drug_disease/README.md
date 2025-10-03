## OTs drug-disease compounds data

These scripts format data from the Open Targets data releases, consisting of the tables which detail the drug - indication, and drug - molecule information stored in the OTs platform.

It is assumed that the following files will be downloaded, for example via FTP at _https://partner-platform.opentargets.org/downloads_
(1.) Read-in download of OTs drug indication data
        - OTs data accessed at ftp://ftp.ebi.ac.uk/pub/databases/opentargets/platform/25.09/output/drug_indication
(2.) Read-in download of OTs drug molecule data
        - OTs data accessed at ftp://ftp.ebi.ac.uk/pub/databases/opentargets/platform/25.09/output/drug_molecule
(3.) Desired output: triple format suitable for KG ingestion

To generate the concatenated data file, first execute *ot_drug_data.py*
Following this, files are formatted ready to ingestion into neo4j using *triple_formatting.py*
This second py file has been kept separate in hopes that it can be repurposed if of use to others.
