# OncoDB

This script creates a graph from [OncoDB's](https://oncodb.org/) gene expression and methylation data.


## Running the script

You need [`uv`](https://docs.astral.sh/uv/) to get started:

```python
$ uv run make_oncodb_graph.py
```

The script:

* Downloads expression and methylation bulk data zip files from OncoDB
* Filters genes to include only significant associations (p < 0.05) after FDR correction
* OncoDB's disease codes are remapped to [Disease Ontology](https://disease-ontology.org/) and [EFO](https://www.ebi.ac.uk/efo/) terms
* Two plain text files are output, containing nodes and edges.

All data processing is done with [duckdb](https://duckdb.org/). `uv` will automatically install all dependencies thanks to [PEP723](https://peps.python.org/pep-0723/). 

## Outputs 

The node and edge lists [are available to download](https://osf.io/6qavy)
