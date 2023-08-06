# Lightweight RDF Stream Parser for Python

A lightweight RDF parser which streams triples directly from disk or standard
input without loading the entire graph into memory.


Work in progress. Only supports ntriple format as of now.

## Usage

Read and write to disk.

```python
from rdf.io import NTriple
from rdf.terms import Literal

with NTriple(path = "./pizzacats.nt", mode = 'r') as g:
    with NTriple(path = "./out.nt", mode = 'w') as h:
        for subject, predicate, object in g.parse():
            if type(object) = Literal and object.language == "en":
                # do stuff
            h.write((subject, predicate, object))
```

Read / write from standard input / output.

```python
from os import stdin
from rdf.io import NTriple
from rdf.terms import IRIRef

g = NTriple(data=stdin.read(), mode = 'r')
h = NTriple(mode = 'w')

target = IRIRef("https://example.org/Pizzacat")
for triple in g.parse():
    if triple[0] == target:
        # do stuff
        h.write(triple)
        
g.close()
h.close()
```
