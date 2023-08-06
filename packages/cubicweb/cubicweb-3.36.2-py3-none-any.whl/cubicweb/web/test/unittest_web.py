# copyright 2003-2014 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
# contact https://www.logilab.fr/ -- mailto:contact@logilab.fr
#
# This file is part of CubicWeb.
#
# CubicWeb is free software: you can redistribute it and/or modify it under the
# terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 2.1 of the License, or (at your option)
# any later version.
#
# CubicWeb is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.
#
# You should have received a copy of the GNU Lesser General Public License along
# with CubicWeb.  If not, see <https://www.gnu.org/licenses/>.

import collections
import hashlib
import tempfile
from json import loads
from os.path import join

from logilab.common.testlib import TestCase, unittest_main
from webtest.forms import Upload

from cubicweb.devtools.fake import FakeRequest
from cubicweb.pyramid.test import PyramidCWTest


class AjaxReplaceUrlTC(TestCase):
    def test_ajax_replace_url_1(self):
        self._test_arurl(
            "fname=view&rql=Person%20P&vid=list", rql="Person P", vid="list"
        )

    def test_ajax_replace_url_2(self):
        self._test_arurl(
            "age=12&fname=view&name=bar&rql=Person%20P&vid=oneline",
            rql="Person P",
            vid="oneline",
            name="bar",
            age=12,
        )

    def _test_arurl(self, qs, **kwargs):
        req = FakeRequest()
        arurl = req.ajax_replace_url
        # NOTE: for the simplest use cases, we could use doctest
        url = arurl("foo", **kwargs)
        self.assertTrue(url.startswith("javascript:"))
        self.assertTrue(url.endswith("()"))
        cbname = url.split()[1][:-2]
        self.assertMultiLineEqual(
            'function %s() { $("#foo").loadxhtml("http://testing.fr/cubicweb/ajax?%s",'
            '{"pageid": "%s"},"get","replace"); }' % (cbname, qs, req.pageid),
            req.html_headers.post_inlined_scripts[0],
        )


class FileUploadTC(PyramidCWTest):
    def _fobject(self, fname):
        return open(join(self.datadir, fname), "rb")

    def _fcontent(self, fname):
        with self._fobject(fname) as f:
            return f.read()

    def _fhash(self, fname):
        content = self._fcontent(fname)
        return hashlib.md5(content).hexdigest()

    def test_single_file_upload(self):
        webreq = self.webapp.post(
            "/ajax?fname=fileupload",
            collections.OrderedDict(
                [("file", Upload("schema.py", self._fobject("schema.py").read()))]
            ),
        )

        # check backward compat : a single uploaded file leads to a single
        # 2-uple in the request form
        expect = {
            "fname": "fileupload",
            "file": ["schema.py", self._fhash("schema.py")],
        }

        body = loads(webreq.body)
        del body["csrf_token"]

        self.assertEqual(webreq.status_code, 200)
        self.assertDictEqual(expect, body)

    def test_multiple_file_upload(self):
        files = [
            ("files", Upload("schema.py", self._fobject("schema.py").read())),
            ("files", Upload("views.py", self._fobject("views.py").read())),
        ]

        webreq = self.webapp.post(
            "/ajax?fname=fileupload",
            files,
            headers={"X-CSRF-Token": self.webapp.get_csrf_token()},
        )

        expect = {
            "fname": "fileupload",
            "files": [
                ["schema.py", self._fhash("schema.py")],
                ["views.py", self._fhash("views.py")],
            ],
        }
        self.assertEqual(webreq.status_code, 200)
        self.assertDictEqual(expect, loads(webreq.text))


class LanguageTC(PyramidCWTest):
    def test_language_neg(self):
        headers = {"Accept-Language": "fr"}
        webreq = self.webapp.get("/", headers=headers)
        webreq.mustcontain(b'lang="fr"')
        vary = [h.lower().strip() for h in webreq.headers.get("Vary").split(",")]
        self.assertIn("accept-language", vary)
        headers = {"Accept-Language": "en"}
        webreq = self.webapp.get("/", headers=headers)
        webreq.mustcontain(b'lang="en"')
        vary = [h.lower().strip() for h in webreq.headers.get("Vary").split(",")]
        self.assertIn("accept-language", vary)

    def test_response_codes(self):
        with self.admin_access.client_cnx() as cnx:
            admin_eid = cnx.user.eid
        # guest can't see admin
        request = self.webapp.get("/%d" % admin_eid, status=403)
        self.assertEqual(request.status_code, 403)

        # but admin can
        self.login()
        request = self.webapp.get("/%d" % admin_eid)
        self.assertEqual(request.status_code, 200)

    def test_session_cookie_httponly(self):
        webreq = self.webapp.get("/")
        self.assertIn("HttpOnly", "".join(webreq.headers.getall("Set-Cookie")))


class MiscOptionsTC(PyramidCWTest):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.logfile = tempfile.NamedTemporaryFile()

    @classmethod
    def init_config(cls, config):
        super().init_config(config)
        config.global_set_option("query-log-file", cls.logfile.name)
        config.global_set_option("datadir-url", "//static.testing.fr/")
        # call load_configuration again to let the config reset its datadir_url
        config.load_configuration()

    def test_log_queries(self):
        self.webapp.get("/")
        self.assertTrue(self.logfile.read())

    def test_datadir_url(self):
        webreq = self.webapp.get("/")
        self.assertNotIn(b"/data/", webreq.body)

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        cls.logfile.close()


if __name__ == "__main__":
    unittest_main()
