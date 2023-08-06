import http.client

from logilab.common.testlib import Tags
from pyramid.httpexceptions import HTTPSeeOther

from cubicweb.pyramid.test import PyramidCWTest


class CWTTC(PyramidCWTest):
    def test_response(self):
        response = self.webapp.get("/")
        self.assertEqual(200, response.status_int)

    def test_base_url(self):
        if self.config["base-url"] not in self.webapp.get("/").text:
            self.fail("no mention of base url in retrieved page")


class CWTIdentTC(PyramidCWTest):
    test_db_id = "webtest-ident"
    anonymous_allowed = False
    tags = PyramidCWTest.tags | Tags(("auth",))

    def test_reponse_denied(self):
        res = self.webapp.get("/", expect_errors=True)
        self.assertEqual(HTTPSeeOther.code, res.status_int)

    def test_login(self):
        self.login(self.admlogin, self.admpassword)
        res = self.webapp.get("/")
        self.assertEqual(http.client.OK, res.status_int)

        self.logout()
        res = self.webapp.get("/", expect_errors=True)
        self.assertEqual(HTTPSeeOther.code, res.status_int)


if __name__ == "__main__":
    import unittest

    unittest.main()
