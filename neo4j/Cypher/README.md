# Cypher code to load data into Neo4j

## Drug -> Disease data

Data files location: [Github](https://github.com/collaborativebioinformatics/GeNETwork/tree/main/data_processing/OTs_drugdis_data)

Cypher code to load data:

```
LOAD CSV WITH HEADERS FROM "file:///drugs.csv" AS row
MERGE (d:Drug {id: row.id})
SET d.name = row.name, d.isApproved = toBoolean(row.isApproved), d.hasBeenWithdrawn = toBoolean(row.hasBeenWithdrawn);

LOAD CSV WITH HEADERS FROM "file:///diseases.csv" AS row
MERGE (ds:Disease {id: row.id})
SET ds.name = row.name;

LOAD CSV WITH HEADERS FROM "file:///drug_disease_interactions.csv" AS row
MATCH (d:Drug {id: row.subject})
MATCH (ds:Disease {id: row.object})
MERGE (d)-[r:INTERACTS_WITH]->(ds)
SET r.maxClinicalTrialPhase = toInteger(row.maxClinicalTrialPhase);
```

Example Cypher code to query data:

```
MATCH p=()-[r:INTERACTS_WITH]->() RETURN p LIMIT 1000
```

## Gene -> Pathway data

Data files location: Data files location: _OSF Storage / outputs_v1 / pathways_triples.tsv (TSV file)_

Cypher code to load data:

```
CREATE CONSTRAINT gene_name_unique IF NOT EXISTS
FOR (g:Gene) REQUIRE g.name IS UNIQUE;
CREATE CONSTRAINT pathway_name_unique IF NOT EXISTS
FOR (p:Pathway) REQUIRE p.name IS UNIQUE;
LOAD CSV WITH HEADERS FROM 'file:///pathways_triples.tsv' AS row
FIELDTERMINATOR '\t'
WITH row WHERE row.gene IS NOT NULL AND row.pathway IS NOT NULL
MERGE (g:Gene {name: row.gene})
MERGE (p:Pathway {name: row.pathway})
MERGE (g)-[:MEMBER_OF {source: row.source}]->(p);
```

Example Cypher code to query data (Focus on a Specific gene):

```
MATCH (g:Gene {name: "TP53"})-[r:MEMBER_OF]->(p:Pathway)
RETURN g,r,p
LIMIT 10;
```

## Gene -> Disease data

Data files location: _OSF Storage / oncodb / oncodb.zip (ZIP file)_

Cypher code to load data:

```
LOAD CSV WITH HEADERS FROM "file:///oncodb/label=Gene/data_0.csv" AS row
MERGE (d:Gene {name: row.name});

LOAD CSV WITH HEADERS FROM "file:///oncodb/label=Disease/data_0.csv" AS row
MERGE (d:Disease {id: row.id})
SET d.name = row.name;

LOAD CSV WITH HEADERS FROM "file:///oncodb/edges.csv" AS row
MATCH (d:Gene {name: row.from})
MATCH (ds:Disease {name: row.to})
MERGE (d)-[r:ASSOCIATED]->(ds)
SET r.data_type = toInteger(row.data_type)
SET r.p = row.p
SET r.change = row.change;
```

## Variant -> Cohort data

Data files location: _OSF Storage / TCGA_data (Folder)_

Cypher code to load data:

```
LOAD CSV WITH HEADERS FROM "file:///tcga/variants.csv" AS row
MERGE (d:Variant {name: row.variant});

LOAD CSV WITH HEADERS FROM "file:///tcga/cohorts.csv" AS row
MERGE (d:Cohort {name: row.cohort});

LOAD CSV WITH HEADERS FROM "file:///tcga/variant_cohort.csv" AS row
MATCH (v:Variant {name: row.subject})
MATCH (c:Cohort {name: row.object})
MERGE (v)-[r:OBSERVED_IN]->(c);
```

