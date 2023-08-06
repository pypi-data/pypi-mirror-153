from cubicweb.devtools.testlib import CubicWebTC
from cubicweb.pyramid.test import PyramidCWTest
from cubicweb.web.views.basecontrollers import ViewController


class ControllerWithCSRFCheckDisabled(ViewController):
    require_csrf = False


class CustomControllerWithoutCSRFTest(PyramidCWTest, CubicWebTC):
    def test_controller_without_csrf(self):
        self.webapp.login()

        # failed with 400 because we didn't send the csrf token
        self.webapp.post(
            f"/cwuser/{self.webapp.admin_login}",
            params={},
            do_not_grab_the_crsf_token=True,
            do_not_inject_origin=True,
            status=400,
        )

        # activate the custom controller that has require_csrf = False
        self.vreg.register_and_replace(ControllerWithCSRFCheckDisabled, ViewController)

        # request works without the csrf token
        self.webapp.post(
            f"/cwuser/{self.webapp.admin_login}",
            params={},
            do_not_grab_the_crsf_token=True,
            do_not_inject_origin=True,
        )

        # request works without the csrf token
        self.webapp.post_json(
            f"/cwuser/{self.webapp.admin_login}",
            params={},
            do_not_grab_the_crsf_token=True,
            do_not_inject_origin=True,
        )


class CSRFTest(PyramidCWTest, CubicWebTC):
    def test_pyramid_route_csrf_token_is_present(self):
        res = self.webapp.get("/login")
        self.assertIn("csrf_token", res.form.fields)

    def test_pyramid_route_csrf_bad_token(self):
        self.webapp.post(
            "/login",
            {
                "__login": self.admlogin,
                "__password": self.admpassword,
                "csrf_token": "bad_token",
            },
            status=400,
        )

    def test_pyramid_route_csrf_no_token(self):
        self.webapp.post(
            "/login",
            {
                "__login": self.admlogin,
                "__password": self.admpassword,
                "csrf_token": None,
            },
            status=400,
        )

    def test_pyramid_route_csrf_bad_origin(self):
        self.webapp.post(
            "/login",
            {"__login": self.admlogin, "__password": self.admpassword},
            headers={"Origin": "bad_origin.net"},
            status=400,
        )

    def test_pyramid_route_csrf_no_origin(self):
        self.webapp.post(
            "/login",
            {"__login": self.admlogin, "__password": self.admpassword},
            do_not_inject_origin=True,
            status=400,
        )

    def test_cubicweb_route_csrf_token_is_present(self):
        self.webapp.post(
            "/validateform",
            {
                "__form_id": "edition",
                "__type:6": "CWUser",
                "eid": 6,
                "firstname-subject:6": "loutre",
            },
        )

    def test_cubicweb_route_no_csrf_token(self):
        self.webapp.post(
            "/validateform",
            {
                "__form_id": "edition",
                "__type:6": "CWUser",
                "eid": 6,
                "firstname-subject:6": "loutre",
                "csrf_token": None,
            },
            status=400,
        )

    def test_cubicweb_route_bad_origin(self):
        self.webapp.post(
            "/validateform",
            {
                "__form_id": "edition",
                "__type:6": "CWUser",
                "eid": 6,
                "firstname-subject:6": "loutre",
            },
            headers={"Origin": "bad_origin.net"},
            status=400,
        )

    def test_cubicweb_route_csrf_no_origin(self):
        self.webapp.post(
            "/validateform",
            {
                "__form_id": "edition",
                "__type:6": "CWUser",
                "eid": 6,
                "firstname-subject:6": "loutre",
            },
            do_not_inject_origin=True,
            status=400,
        )

    def test_pyramid_route_csrf_token_post_json(self):
        self.webapp.login()
        self.webapp.post_json(
            f"/cwuser/{self.webapp.admin_login}",
            params={},
            status=200,
        )
