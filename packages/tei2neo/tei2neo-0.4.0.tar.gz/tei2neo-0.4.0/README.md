# TEI parser

This is a parser written in Python 3 that takes TEI-XML Documents as an inpput and writes them in a [Neo4j Graph Database](https://neo4j.com).

It makes use of the following existing libraries:

* [Beautiful Soup 4](https://beautiful-soup-4.readthedocs.io/en/latest/) An easy-to-use XML parser
* [Spacy](https://spacy.io). Currently we use the german language package `de_core_news_sm` to parse the text.
* [Py2neo v4](https://py2neo.org/v4/) whih is a library to work with the Neo4j database.

## Installation

```
$ pip install tei2neo
$ python -m spacy download de_core_news_sm
```


## Synopsis

```
from tei2neo import parse, GraphUtils
graph = Graph(host="localhost", user="neo4j", password="password")
doc, status, soup = parse(
	filename=file, 
	start_with_tag='TEI', 
	idno='20-MS-221'
)
tx = graph.begin()
doc.save(tx)
tx.commit()

ut = GraphUtils(graph)
paras = ut.paragraphs_for_filename('20_MS_221_1.xml')

# create unhyphened tokens
for para in paras:
    tokens = ut.tokens_in_paragraph(para)
    ut.create_unhyphenated(tokens)
    
# show hyphened text
for token in ut.tokens_in_paragraph(paras[5], concatenated=0):
    if 'lb' in token.labels:
        print(' | ', end='')
    print(token.get('string',''), end='')
    print(token.get('whitespace', ''), end='')
    
# show concatenated (non-hyphened) version of the text
for token in ut.tokens_in_paragraph(paras[5], concatenated=1):
    if 'lb' in token.labels:
        print(' ', end='')

    print(token.get('string',''), end='')
    print(token.get('whitespace', ''), end='')
```

# How the parser works

A TEI document can be constructed in various ways and there are many elements that work very similarly. Likewise, this parser expects certain elements and treats them in a specific manner.

## Elements that affect all following elements

### handShift

A `handShift` element **affects all elements that are below**, until another `handShift` element is encountered. 

**Example**

From now on everything is written in «Latein» and a pencil is being used (medium=Blei):
```
<handShift new="#hWH" medium="Blei" script="Latein"/>
```

Now we switch to «Kurrent» script and use black ink (STinte):

```
<handShift new="#hGS" medium="STinte" script="Kurrent"/>
```
**Appearance in Neo4j**

As we have seen, a `handShift` element contains three attributes:

* new="#hWH"
* medium="Blei"
* script="Latein"

These attributes are passed to all Token elements that follow after a `handShift` occurs. Previous attributes are not deleted, i.e. if only the medium changes from «Blei» to «STinte», all other attributes stay the same.
The `handShift` element will *not* appear as a node in Neo4j.


### delSpan

A `delSpan` element works much like a `handShift` element, as it alters the appearance of all the following text until it reaches its `spanTo` target:

```
<delSpan spanTo="#A20_MS_215_12_3"/>
... (a lot of XML code here)
<anchor xml:id="A20_MS_215_12_3"/>
```

**Appearance in Neo4j**

* both the `delSpan` and the `anchor` appear as additional nodes.
* all elements between the `delSpan` and the `anchor` element receive an additional `delSpan` label
* a `delSpan` attribute is added to every element, the value is equal to the `xml:id` attribute of the anchor.
