from rdflib import Graph

from cubicweb.pyramid.test import PyramidCWTest

_MIMETYPES = [
    "application/rdf+xml",
    "text/turtle",
    "text/n3",
    "application/n-quads",
    "application/n-triples",
    "application/trig",
    "application/ld+json",
]


class ContentNegociationTC(PyramidCWTest):
    def setup_database(self):
        with self.admin_access.repo_cnx() as cnx:
            self.blog = cnx.create_entity(
                "Blog",
                title="CubicWeb Blog",
            )
            self.blog_entry = cnx.create_entity(
                "BlogEntry",
                title="une news !",
                content="cubicweb c'est beau",
                unique_id=42,
                entry_of=self.blog,
            )
            cnx.commit()

    def _check_alternate_links(self, res):
        links = res.headers.getall("Link")
        html_links = [str(x) for x in res.html.find_all("link")]
        rest_path = self.blog_entry.rest_path()
        for mimetype in _MIMETYPES:
            assert (
                f"<http://testing.fr/cubicweb/{rest_path}>;rel=alternate;type={mimetype}"
                in links
            )
            assert (
                f'<link href="http://testing.fr/cubicweb/{rest_path}" rel="alternate"'
                f' title="{mimetype}" type="{mimetype}"/>' in html_links
            )

    def test_content_negociation_link_alternate_etype_rest_attr(self):
        self.login()
        res = self.webapp.get(f"/BlogEntry/{self.blog_entry.unique_id}")
        self._check_alternate_links(res)
        # check if result is HTML content
        assert res.html

    def test_content_negociation_link_alternate_etype_eid(self):
        self.login()
        # the resource does not exist since a "rest_attr" is defined for BlogEntry
        res = self.webapp.get(f"/BlogEntry/{self.blog_entry.eid}", status=404)
        assert res.html
        assert "<h1>this resource does not exist</h1>" in res.body.decode("utf-8")

    def test_content_negociation_link_alternate_eid(self):
        self.login()
        res = self.webapp.get(f"/{self.blog_entry.eid}")
        self._check_alternate_links(res)
        # check if result is HTML content
        assert res.html

    def test_content_negociation_404_with_eid(self):
        """The /etype/eid route is disabled if rest_attr if defined"""
        self.login()
        res = self.webapp.get(
            f"/BlogEntry/{self.blog_entry.eid}",
            headers={"Accept": "text/n3"},
            status=404,
        )
        # check if result is HTML content
        assert res.html
        assert "<h1>this resource does not exist</h1>" in res.body.decode("utf-8")

    def test_content_negociation_wrong_accept(self):
        self.login()
        res = self.webapp.get(f"/{self.blog_entry.eid}", headers={"Accept": "text/n4"})
        # the predicate 'is_request_mimetype_rdf_format' answer false then CubicWeb return
        # html content from primary view
        assert res.html

    def test_content_negociation_rest_attr(self):
        self.login()
        res = self.webapp.get(
            f"/BlogEntry/{self.blog_entry.unique_id}", headers={"Accept": "text/n3"}
        )
        g = Graph()
        g.parse(data=res.body.decode("utf-8"), format="text/n3")
        ask_res = g.query(
            f"""
            ASK {{
                <http://testing.fr/cubicweb/{self.blog_entry.eid}>
                    a <http://ns.cubicweb.org/cubicweb/0.0/BlogEntry>;
                    <http://ns.cubicweb.org/cubicweb/0.0/title> "{self.blog_entry.title}";
                    <http://ns.cubicweb.org/cubicweb/0.0/content> "{self.blog_entry.content}".
            }}"""
        )
        assert ask_res.askAnswer

    def test_content_negociation_etype_eid(self):
        self.login()
        res = self.webapp.get(f"/Blog/{self.blog.eid}", headers={"Accept": "text/n3"})
        g = Graph()
        g.parse(data=res.body.decode("utf-8"), format="text/n3")
        ask_res = g.query(
            f"""
            ASK {{
                <http://testing.fr/cubicweb/{self.blog.eid}>
                    a <http://ns.cubicweb.org/cubicweb/0.0/Blog>;
                    <http://ns.cubicweb.org/cubicweb/0.0/title> "{self.blog.title}".
            }}"""
        )
        assert ask_res.askAnswer

    def test_content_negociation_jsonld_triples_content(self):
        self.login()
        res = self.webapp.get(
            f"/BlogEntry/{self.blog_entry.unique_id}",
            headers={"Accept": "application/ld+json"},
        )
        g = Graph()
        g.parse(data=res.body.decode("utf-8"), format="json-ld")
        ask_res = g.query(
            f"""
            ASK {{
                <http://testing.fr/cubicweb/{self.blog_entry.eid}>
                    a <http://ns.cubicweb.org/cubicweb/0.0/BlogEntry>;
                    <http://ns.cubicweb.org/cubicweb/0.0/title> "{self.blog_entry.title}";
                    <http://ns.cubicweb.org/cubicweb/0.0/content> "{self.blog_entry.content}".
            }}"""
        )
        assert ask_res.askAnswer
