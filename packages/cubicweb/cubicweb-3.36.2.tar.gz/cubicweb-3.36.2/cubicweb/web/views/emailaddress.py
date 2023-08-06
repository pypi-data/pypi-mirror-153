# copyright 2003-2010 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
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
"""Specific views for email addresses entities"""


from cubicweb import Unauthorized
from cubicweb.predicates import is_instance
from cubicweb.schema import display_name
from cubicweb.web.views import uicfg, baseviews, primary, ibreadcrumbs

_pvs = uicfg.primaryview_section
_pvs.tag_subject_of(("*", "use_email", "*"), "attributes")
_pvs.tag_subject_of(("*", "primary_email", "*"), "hidden")


class EmailAddressPrimaryView(primary.PrimaryView):
    __select__ = is_instance("EmailAddress")

    def cell_call(self, row, col, skipeids=None):
        self.skipeids = skipeids
        super().cell_call(row, col)

    def render_entity_attributes(self, entity):
        self.w("<h3>")
        entity.view("oneline", w=self.w)
        if entity.prefered:
            self.w("&#160;(<i>%s</i>)", entity.prefered.view("oneline"), escape=False)
        self.w("</h3>")
        try:
            persons = entity.reverse_primary_email
        except Unauthorized:
            persons = []
        if persons:
            emailof = persons[0]
            self.field(
                display_name(self._cw, "primary_email", "object"),
                emailof.view("oneline"),
            )
            pemaileid = emailof.eid
        else:
            pemaileid = None
        try:
            emailof = (
                "use_email" in self._cw.vreg.schema and entity.reverse_use_email or ()
            )
            emailof = [e for e in emailof if not e.eid == pemaileid]
        except Unauthorized:
            emailof = []
        if emailof:
            emailofstr = ", ".join(e.view("oneline") for e in emailof)
            self.field(display_name(self._cw, "use_email", "object"), emailofstr)

    def render_entity_relations(self, entity):
        for i, email in enumerate(entity.related_emails(self.skipeids)):
            self.w('<div class="%s">', i % 2 and "even" or "odd")
            email.view("oneline", w=self.w, contexteid=entity.eid)
            self.w("</div>")


class EmailAddressShortPrimaryView(EmailAddressPrimaryView):
    __select__ = is_instance("EmailAddress")
    __regid__ = "shortprimary"
    title = None  # hidden view

    def render_entity_attributes(self, entity):
        self.w("<h5>")
        entity.view("oneline", w=self.w)
        self.w("</h5>")


class EmailAddressOneLineView(baseviews.OneLineView):
    __select__ = is_instance("EmailAddress")

    def entity_call(self, entity, **kwargs):
        if entity.reverse_primary_email:
            self.w("<b>")
        if entity.alias:
            self.w("%s &lt;", entity.alias)
        self.w('<a href="%s">%s</a>', entity.absolute_url(), entity.display_address())
        if entity.alias:
            self.w("&gt;\n")
        if entity.reverse_primary_email:
            self.w("</b>")


class EmailAddressMailToView(baseviews.OneLineView):
    """A one line view that builds a user clickable URL for an email with
    'mailto:'"""

    __regid__ = "mailto"
    __select__ = is_instance("EmailAddress")

    def entity_call(self, entity, **kwargs):
        if entity.reverse_primary_email:
            self.w("<b>")
        if entity.alias:
            alias = entity.alias
        elif entity.reverse_use_email:
            alias = entity.reverse_use_email[0].dc_title()
        else:
            alias = None
        if alias:
            mailto = f"mailto:{alias} <{entity.display_address()}>"
        else:
            mailto = "mailto:%s" % entity.display_address()
        self.w('<a href="%s">%s</a>', mailto, entity.display_address())
        if entity.reverse_primary_email:
            self.w("</b>")


class EmailAddressInContextView(baseviews.InContextView):
    __select__ = is_instance("EmailAddress")

    def cell_call(self, row, col, **kwargs):
        if self._cw.vreg.config["mangle-emails"]:
            self.wview("oneline", self.cw_rset, row=row, col=col, **kwargs)
        else:
            self.wview("mailto", self.cw_rset, row=row, col=col, **kwargs)


class EmailAddressTextView(baseviews.TextView):
    __select__ = is_instance("EmailAddress")

    def cell_call(self, row, col, **kwargs):
        self.w(self.cw_rset.get_entity(row, col).display_address())


class EmailAddressIBreadCrumbsAdapter(ibreadcrumbs.IBreadCrumbsAdapter):
    __select__ = is_instance("EmailAddress")

    def parent_entity(self):
        return self.entity.email_of
