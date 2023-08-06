# copyright 2003-2012 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
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
"""security management and error screens"""


import sys
import traceback

from logilab.common.registry import yes
from logilab.mtconverter import xml_escape

from cubicweb import _
from cubicweb.predicates import none_rset, match_user_groups, authenticated_user
from cubicweb.uilib import html_traceback, rest_traceback, exc_message
from cubicweb.view import AnyRsetView, EntityView, View
from cubicweb.web import formwidgets as wdgs
from cubicweb.web.formfields import guess_field
from cubicweb.web.views.schema import SecurityViewMixIn

SUBMIT_MSGID = _("Submit bug report")
MAIL_SUBMIT_MSGID = _("Submit bug report by mail")


class SecurityManagementView(SecurityViewMixIn, EntityView):
    """display security information for a given entity"""

    __regid__ = "security"
    __select__ = EntityView.__select__ & authenticated_user()

    title = _("security")

    def call(self):
        self.w('<div id="progress">%s</div>', self._cw._("validating..."))
        super(SecurityManagementView, self).call()

    def entity_call(self, entity):
        self._cw.add_js("cubicweb.edition.js")
        self._cw.add_css("cubicweb.acl.css")
        _ = self._cw._
        self.w(
            '<h1><span class="etype">%s</span> <a href="%s">%s</a></h1>',
            entity.dc_type().capitalize(),
            entity.absolute_url(),
            entity.dc_title(),
        )
        # first show permissions defined by the schema
        self.w("<h2>%s</h2>", _("Schema's permissions definitions"))
        self.permissions_table(entity.e_schema)
        self.w("<h2>%s</h2>", _("Manage security"))
        # ownership information
        if self._cw.vreg.schema.relation_schema_for("owned_by").has_perm(
            self._cw, "add", fromeid=entity.eid
        ):
            self.owned_by_edit_form(entity)
        else:
            self.owned_by_information(entity)

    def owned_by_edit_form(self, entity):
        self.w("<h3>%s</h3>", self._cw._("Ownership"))
        msg = self._cw._("ownerships have been changed")
        form = self._cw.vreg["forms"].select(
            "base",
            self._cw,
            entity=entity,
            form_renderer_id="onerowtable",
            submitmsg=msg,
            form_buttons=[wdgs.SubmitButton()],
            domid="ownership%s" % entity.eid,
            __redirectvid="security",
            __redirectpath=entity.rest_path(),
        )
        field = guess_field(
            entity.e_schema, self._cw.vreg.schema["owned_by"], req=self._cw
        )
        form.append_field(field)
        form.render(w=self.w, display_progress_div=False)

    def owned_by_information(self, entity):
        ownersrset = entity.related("owned_by")
        if ownersrset:
            self.w("<h3>%s</h3>", self._cw._("Ownership"))
            self.w('<div class="ownerInfo">')
            self.w(self._cw._("this entity is currently owned by"), " ")
            self.wview("csv", entity.related("owned_by"), "null")
            self.w("</div>")
        # else we don't know if this is because entity has no owner or becayse
        # user as no access to owner users entities


class ErrorView(AnyRsetView):
    """default view when no result has been found"""

    __select__ = yes()
    __regid__ = "error"

    def page_title(self):
        """returns a title according to the result set - used for the
        title in the HTML header
        """
        return self._cw._("an error occurred")

    def _excinfo(self):
        req = self._cw
        ex = req.data.get("ex")
        excinfo = req.data.get("excinfo")
        if "errmsg" in req.data:
            errmsg = req.data["errmsg"]
            exclass = None
        else:
            errmsg = exc_message(ex, req.encoding)
            exclass = ex.__class__.__name__
        return errmsg, exclass, excinfo

    def call(self):
        req = self._cw.reset_headers()
        title = self._cw._("an error occurred")
        self.w("<h2>%s</h2>", title)

        ex, exclass, excinfo = self._excinfo()
        # save excinfo on req for easier debugging in interactive shell
        req.excinfo = ex, exclass, excinfo

        if excinfo is not None and self._cw.vreg.config["print-traceback"]:
            if exclass is None:
                self.w(
                    '<div class="tb">%s</div>',
                    xml_escape(ex).replace("\n", "<br />"),
                    escape=False,
                )
            else:
                self.w(
                    '<div class="tb">%s: %s</div>',
                    xml_escape(exclass),
                    xml_escape(ex).replace("\n", "<br />"),
                    escape=False,
                )
            self.w("<hr />")
            self.w(
                '<div class="tb">%s</div>',
                html_traceback(excinfo, ex, ""),
                escape=False,
            )
        else:
            self.w(
                '<div class="tb">%s</div>',
                xml_escape(ex).replace("\n", "<br />"),
                escape=False,
            )

        # if excinfo is not None, it's probably not a bug
        if excinfo is None:
            return

        # displaying the exception of stderr for debugging
        traceback.print_tb(tb=excinfo[-1])
        print()
        print(excinfo[1], file=sys.stderr)

        if self._cw.cnx:
            vcconf = self._cw.cnx.repo.get_versions()
            self.w("<div>")
            eversion = vcconf.get("cubicweb", self._cw._("no version information"))
            # NOTE: tuple wrapping needed since eversion is itself a tuple
            self.w("<b>CubicWeb version:</b> %s<br/>\n", eversion)
            cversions = []
            for cube in self._cw.vreg.config.cubes():
                cubeversion = vcconf.get(cube, self._cw._("no version information"))
                self.w("<b>Cube %s version:</b> %s<br/>\n", cube, cubeversion)
                cversions.append((cube, cubeversion))
            self.w("</div>")
        else:
            eversion = self._cw._("no version information")
            cversions = []
        # creates a bug submission link if submit-mail is set
        if self._cw.vreg.config["submit-mail"]:
            form = self._cw.vreg["forms"].select(
                "base", self._cw, rset=None, mainform=False
            )
            binfo = text_error_description(ex, excinfo, req, eversion, cversions)
            form.add_hidden(
                "description",
                binfo,
                # we must use a text area to keep line breaks
                widget=wdgs.TextArea({"class": "hidden"}),
            )
            # add a signature so one can't send arbitrary text
            form.add_hidden("__signature", req.vreg.config.sign_text(binfo))
            form.add_hidden("__bugreporting", "1")
            form.form_buttons = [wdgs.SubmitButton(MAIL_SUBMIT_MSGID)]
            form.action = req.build_url("reportbug")
            form.render(w=self.w)


def text_error_description(ex, excinfo, req, eversion, cubes):
    binfo = rest_traceback(excinfo, xml_escape(ex))
    binfo += "\n\n:URL: %s\n" % req.url()
    if "__bugreporting" not in req.form:
        binfo += "\n:form params:\n"
        binfo += "\n".join("  * %s = %s" % (k, v) for k, v in req.form.items())
    binfo += "\n\n:CubicWeb version: %s\n" % (eversion,)
    for pkg, pkgversion in cubes:
        binfo += ":Cube %s version: %s\n" % (pkg, pkgversion)
    binfo += "\n"
    return binfo


class CwStats(View):
    """A textual stats output for monitoring tools such as munin"""

    __regid__ = "processinfo"
    content_type = "text/plain"
    templatable = False
    __select__ = none_rset() & match_user_groups("users", "managers")

    def call(self):
        stats = self._cw.call_service("repo_stats")
        stats["threads"] = ", ".join(sorted(stats["threads"]))
        for k in stats:
            if k in ("extid_cache_size", "type_source_cache_size"):
                continue
            if k.endswith("_cache_size"):
                stats[k] = "%s / %s" % (stats[k]["size"], stats[k]["maxsize"])
        results = []
        for element in stats:
            results.append("%s %s" % (element, stats[element]))
        self.w("\n".join(results))
