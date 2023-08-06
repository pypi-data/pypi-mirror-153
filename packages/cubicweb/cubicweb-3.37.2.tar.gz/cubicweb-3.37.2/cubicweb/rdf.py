# copyright 2019 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
# contact https://www.logilab.fr -- mailto:contact@logilab.fr
#
# This program is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 2.1 of the License, or (at your option)
# any later version.
#
# This program is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE. See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with this program. If not, see <https://www.gnu.org/licenses/>.

from rdflib import namespace


RDF_MIMETYPE_TO_FORMAT = {
    "application/rdf+xml": "xml",
    "text/turtle": "turtle",
    "text/n3": "n3",
    "application/n-quads": "nquads",
    "application/n-triples": "nt",
    "application/trig": "trig",
    "application/ld+json": "json-ld",
}

NAMESPACES = {
    "rdf": namespace.RDF,
    "rdfs": namespace.RDFS,
    "owl": namespace.OWL,
    "xsd": namespace.XSD,
    "skos": namespace.SKOS,
    "void": namespace.VOID,
    "dc": namespace.DC,
    "dcterms": namespace.DCTERMS,
    "foaf": namespace.FOAF,
    "doap": namespace.DOAP,
    "schema": namespace.Namespace("http://schema.org/"),
    "cubicweb": namespace.Namespace("http://ns.cubicweb.org/cubicweb/0.0/"),
}


def add_entity_to_graph(graph, entity):
    adapter = entity.cw_adapt_to("rdf")
    if adapter:
        for triple in adapter.triples():
            graph.add(triple)
        for prefix, rdfns in adapter.used_namespaces.items():
            graph.bind(prefix, rdfns)
