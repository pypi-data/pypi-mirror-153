from lxml import etree
parser = etree.XMLParser(dtd_validation=True, recover=True)
from bs4 import BeautifulSoup


def parse_register(filename, entity, tx):
    """Storing register into the graph database.
    """

    def store_person(elem):
	attrs = elem.attrs
	name = elem.find('persName')
	attrs['name'] = name.string
	person_node = Node('person', **attrs)
	tx.create(person_node)
	
	birth = elem.find('birth')
	if birth:
	    attrs = birth.attrs
	    for item in (birth.children):
		if isinstance(item, str):
		    attrs['date'] = item.strip()
		else:
		    settlement = item.find('settlement')
		    if settlement:
			attrs['settlement'] = settlement.string or ''        
	    birth_node = Node('birth', **attrs)
	    rs = Relationship(person_node, 'WAS_BORN', birth_node)
	    tx.create(rs)
	
	death = elem.find('death')
	if death:
	    attrs = death.attrs
	    for item in (death.children):
		if isinstance(item, str):
		    attrs['date'] = item.strip()
		else:
		    settlement = item.find('settlement')
		    if settlement: 
			attrs['settlement'] = settlement.string or ''
	    
	    died_node = Node('death', **attrs)
	    rs = Relationship(person_node, 'DIED', died_node)
	    tx.create(rs)

    def store_place(elem):
        attrs = elem.attrs
	name = elem.find('placeName')
	attrs['name'] = name.string
	
        for subelem in ['country', 'region']:
            for subelem_node in elem.find_all(subelem):
                subelem_attrs = subelem_node.attrs
                attrs = { **attrs, **subelem_attrs }
                if subelem_node.string:
                    attrs[subelem] = subelem_node.string

	place_node = Node('place', **attrs)
	tx.create(place_node)

    def store_artifacts(elem):
        attrs = elem.attrs
        names = []
        for name_node in elem.find_all('name'):
            names.append(name_node.string)

	attrs['name'] = names
	node = Node('artifact', **attrs)
	tx.create(node)

    def store_terms(elem):
        attrs = elem.attrs
        names = []
        for name_node in elem.find_all('term'):
            names.append(name_node.string)

	attrs['name'] = names
	node = Node('term', **attrs)
	tx.create(node)

    def store_biblioindex(elem):
        attrs = elem.attrs

        title = elem.find('title')
        if title: attrs['title'] = title.string

        for attr in ['title','publisher','pubPlace','date']:
            subelem = elem.find(attr)
            if subelem:
                attrs[attr] = subelem.string

        ref = elem.find('ref')
        if ref:
            attrs['ref'] = ref.get('target')

	node = Node('biblStruct', **attrs)
	tx.create(node)


    entity2proc = {
        "person", store_person,
        "place", store_place,
        "artifact", store_artifacts,
        "term", store_terms,
        "biblioindex": store_biblioindex,
    }

    entity2start_with = {
        "person", "listPerson",
        "place", "listPlace",
        "artifact", "list",
        "term", "list",
        "biblioindex", "listBibl",
    }

    parser = etree.XMLParser(dtd_validation=True, recover=True)
    tree = etree.parse(filename, parser)
    unicode_string = etree.tostring(tree.getroot(), encoding='unicode')
    soup = BeautifulSoup(unicode_string, 'lxml-xml')
    start_with = soup.find(entity2start_with[entity])
    store_proc = entity2proc[entity]
    for item in start_with.find_all('entity'):
        store_proc(item)
