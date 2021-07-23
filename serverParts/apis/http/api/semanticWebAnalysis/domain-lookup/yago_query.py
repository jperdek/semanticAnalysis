import rdflib.graph as g
import rdflib
import rdfextras


def test_graph():
    filename = "../../../../../../output/domain-lookup/yagoProcessed/book_strategy1.ttl"
    uri = "Single-entry_bookkeeping_system"

    # Graph.query() can be used now
    rdfextras.registerplugins()

    graph = g.Graph()
    graph.parse(filename, format="turtle")
    results = graph.query("""
    BASE <http://yago-knowledge.org/resource/>
    PREFIX dbp: <http://dbpedia.org/ontology/>
    PREFIX owl: <http://www.w3.org/2002/07/owl#>
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
    PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

    SELECT ?p ?o
    WHERE {
    <%s> ?p ?o.
    }
    ORDER BY (?p)
    """ % uri)

    for result in results:
        print(result)


if __name__ == "__main__":
    test_graph()
