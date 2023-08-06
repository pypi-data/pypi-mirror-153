from cubicweb.pyramid.test import PyramidCWTest


def simple_test_view(request):
    return request.response


class AnonymousDisallowedPredicatesTC(PyramidCWTest):
    anonymous_allowed = False

    def includeme(self, config):
        config.add_route("view-entity", r"/{eid}", has_cw_permission="read")
        config.add_view(simple_test_view, route_name="view-entity")
        config.registry.settings["pyramid.csrf_trusted_origins"] = ["example.com"]

    def setUp(self):
        super(AnonymousDisallowedPredicatesTC, self).setUp()
        with self.admin_access.repo_cnx() as cnx:
            self.eid = self.create_user(cnx, "Fernestin").eid
            cnx.commit()

    def test_view_entity_without_connection(self):
        self.webapp.get(f"/{self.eid}", status=303)

    def test_view_entity_with_connection(self):
        self.login(user="Fernestin", password="Fernestin")
        self.webapp.get(f"/{self.eid}", status=200)


class PredicatesTC(PyramidCWTest):
    def includeme(self, config):
        # to test route predicate
        config.add_route(
            "permission-update-route",
            r"/{eid}/test-permission-update-route",
            has_cw_permission="update",
        )
        config.add_view(simple_test_view, route_name="permission-update-route")
        # to test view predicate
        config.add_route(
            "permission-update-view", r"/{eid}/test-permission-update-view"
        )
        config.add_view(
            simple_test_view,
            route_name="permission-update-view",
            has_cw_permission="update",
        )
        config.registry.settings["pyramid.csrf_trusted_origins"] = ["example.com"]

    def test_has_cw_permission_route_predicate(self):
        with self.admin_access.repo_cnx() as cnx:
            eid = self.create_user(cnx, "Fernestin").eid
            cnx.commit()
        res = self.webapp.get(f"/{eid}/test-permission-update-route", status="*")
        self.assertEqual(res.status_int, 404)
        self.webapp.post(
            "/login", {"__login": self.admlogin, "__password": self.admpassword}
        )
        res = self.webapp.get(f"/{eid}/test-permission-update-route", status="*")
        self.assertEqual(res.status_int, 200)

    def test_has_cw_permission_view_predicate(self):
        with self.admin_access.repo_cnx() as cnx:
            eid = self.create_user(cnx, "Fernestin").eid
            cnx.commit()
        res = self.webapp.get(f"/{eid}/test-permission-update-view", status="*")
        self.assertEqual(res.status_int, 404)
        self.webapp.login(user=self.admlogin, password=self.admpassword)
        res = self.webapp.get(f"/{eid}/test-permission-update-view", status="*")
        self.assertEqual(res.status_int, 200)
