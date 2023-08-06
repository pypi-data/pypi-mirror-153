from unittest import skipUnless

from cubicweb.devtools import testlib

try:
    import docutils  # noqa

    DOCUTILS_AVAILABLE = True
except ImportError:
    DOCUTILS_AVAILABLE = False


class WdocViewsTC(testlib.CubicWebTC):
    @skipUnless(
        DOCUTILS_AVAILABLE, "rest_publish does not support ..winclude without docutils"
    )
    def test(self):
        with self.admin_access.web_request(fid="main") as req:
            page = req.view("wdoc")
        self.assertIn("Site documentation", page)
        # This part is renderend through rst extension (..winclude directive).
        self.assertIn(
            "This web application is based on the CubicWeb knowledge management system",
            page,
        )


if __name__ == "__main__":
    import unittest

    unittest.main()
