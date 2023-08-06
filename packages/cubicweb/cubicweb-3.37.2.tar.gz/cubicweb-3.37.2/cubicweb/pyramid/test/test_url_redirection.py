from cubicweb.pyramid.test import PyramidCWTest


def redirect_rule(req, url, matchdict):
    return f"{url}/test"


class UrlRedirectTC(PyramidCWTest):
    def includeme(self, config):
        config.add_redirection_rule(r"^/\w+$", redirect_rule)

    def test_redirect_rules(self):
        res = self.webapp.get("/123456", status="*")
        self.assertEqual(res.status_int, 303)
        self.assertEqual(res.location, f"{res.request.application_url}/123456/test")


if __name__ == "__main__":
    import unittest

    unittest.main()
