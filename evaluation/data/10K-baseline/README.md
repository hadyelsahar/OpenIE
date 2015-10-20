# 10K-baseline  dataset for open information extraction
a dataset of well selected 10K sentences bootstrapped from the wikipedia articles and
annotated automatically with Ollie system for open information extraction.
then manually filtered later.

## dataset statistics:

- number of sentences : ~11K sentence, one sentence per line
- number of words: 280193 (42580 unique)
- min words per line : 15
- avg word per line : 25

## dataset Notes

Data is created by querying first 10000 abstracts for types persons, countries, capitals and companies types in DBpedia.
The Dataset doesn't evaluate a real usecase of OpenIE systems but rather a simple version of it.

## SPARQL Queries

```
#types used are yago:Company108058098, dbo:Person, yago:Capital108518505, yago:Country108544813

select distinct ?x where {

?y rdf:type [TYPE].
?y dbo:abstract ?x .

FILTER (lang(?x) = 'en')
} LIMIT 10000

```

