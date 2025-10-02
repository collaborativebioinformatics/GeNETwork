# /// script
# dependencies = [
#   "httpx",
# ]
# ///

import httpx

import asyncio
import csv

async def fetch_pgscatalog_traits(url = "https://www.pgscatalog.org/rest/trait/all", efo_terms = None):
    if efo_terms is None:
        efo_terms = []
    async with httpx.AsyncClient() as client:
        resp = await client.get(url)
        resp.raise_for_status()
        json = resp.json()
        if json["results"] is not None:
            efo_terms.extend(json["results"])
        if (url := json["next"]) is not None:
            print (f"Geting {url}")
            return await fetch_pgscatalog_traits(efo_terms=efo_terms, url=url)
        else:
            return efo_terms


def main():
    traits = asyncio.run(fetch_pgscatalog_traits())
    disease_tuples = [(x["id"], x["associated_pgs_ids"]) for x in traits]

    flat = [
        (value, key)
        for key, values in disease_tuples
        for value in values
    ]

    with open('pgscatalog.csv', 'w', newline='\n') as csvfile:
        fieldnames = ["subject", "predicate", "object"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for subject, object in flat:
            writer.writerow({"subject": subject, "predicate": "predicts_disposition", "object": object})

if __name__ == "__main__":
    main()
