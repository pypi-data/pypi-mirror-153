# copyright 2003-2016 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
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
"""default templates for CubicWeb web client"""


from logilab.common.decorators import classproperty
from logilab.common.deprecation import class_renamed
from logilab.common.registry import objectify_predicate
from logilab.mtconverter import xml_escape

from cubicweb._exceptions import NotAnEntity
from cubicweb import _
from cubicweb.predicates import match_kwargs, anonymous_user
from cubicweb.schema import display_name
from cubicweb.utils import UStringIO
from cubicweb.view import View, MainTemplate, NOINDEX, NOFOLLOW, StartupView
from cubicweb.web import formfields as ff, formwidgets as fw
from cubicweb.web.views import forms
from cubicweb.rdf import RDF_MIMETYPE_TO_FORMAT


# main templates ##############################################################


class LogInOutTemplate(MainTemplate):
    def call(self):
        self.set_request_content_type()
        self.write_doctype()
        self.template_header("text/html", self._cw._("login_action"))
        self.w("<body>\n")
        self.content(self.w)
        self.w("</body>")

    def template_header(
        self, content_type, view=None, page_title="", additional_headers=()
    ):
        self._cw.html_headers.define_var("BASE_URL", self._cw.base_url())
        self._cw.html_headers.define_var("DATA_URL", self._cw.datadir_url)
        # explictly close the <base> tag to avoid IE 6 bugs while browsing DOM
        self.whead('<base href="%s"></base>', self._cw.base_url())
        self.whead(
            '<meta http-equiv="content-type" content="%s; charset=%s"/>\n',
            content_type,
            self._cw.encoding,
        )
        self.whead(NOINDEX)
        self.whead(NOFOLLOW)
        self.whead("\n".join(additional_headers) + "\n")
        self.wview("htmlheader", rset=self.cw_rset)
        self.whead("<title>%s</title>\n", xml_escape(page_title))

    def content(self):
        raise NotImplementedError()


class LogInTemplate(LogInOutTemplate):
    __regid__ = "login"
    __select__ = anonymous_user()
    title = "log in"

    def content(self, w):
        self.wview("logform", rset=self.cw_rset, id="loginBox", klass="")


class LoggedOutTemplate(StartupView):
    __regid__ = "loggedout"
    __select__ = anonymous_user()
    title = "logged out"

    def call(self):
        msg = self._cw._("you have been logged out")
        if self._cw.cnx:
            comp = self._cw.vreg["components"].select("applmessages", self._cw)
            comp.render(w=self.w, msg=msg)
            self.wview("index")
        else:
            self.w("<h2>%s</h2>", msg)


@objectify_predicate
def modal_view(cls, req, rset, *args, **kwargs):
    if req.form.get("__modal", None):
        return 1


@objectify_predicate
def templatable_view(cls, req, rset, *args, **kwargs):
    view = kwargs.pop("view", None)
    if view is None:
        return 1
    if view.binary:
        return 0
    if "__notemplate" in req.form:
        return 0
    return view.templatable


class NonTemplatableViewTemplate(MainTemplate):
    """main template for any non templatable views (xml, binaries, etc.)"""

    __regid__ = "main-template"
    __select__ = ~templatable_view()

    def call(self, view):
        view.set_request_content_type()
        view.set_stream()
        if (
            ("__notemplate" in self._cw.form)
            and view.templatable
            and view.content_type == self._cw.html_content_type()
        ):
            view.w("<div>")
            view.render()
            view.w("</div>")
        else:
            view.render()
        # have to replace our stream by view's stream (which may be a binary
        # stream)
        self._stream = view._stream


class ModalMainTemplate(MainTemplate):
    """a no-decoration main template for standard views
    that typically live in a modal context"""

    __regid__ = "main-template"
    __select__ = templatable_view() & modal_view()

    def call(self, view):
        view.set_request_content_type()
        view.render(w=self.w)


class TheMainTemplate(MainTemplate):
    """default main template :

    - call header / footer templates
    """

    __regid__ = "main-template"
    __select__ = templatable_view()

    def call(self, view):
        self.set_request_content_type()
        self.template_header(self.content_type, view)
        self.w('<div id="pageContent">\n')
        vtitle = self._cw.form.get("vtitle")
        if vtitle:
            self.w('<div class="vtitle">%s</div>\n', vtitle)
        # display entity type restriction component
        etypefilter = self._cw.vreg["components"].select_or_none(
            "etypenavigation", self._cw, rset=self.cw_rset
        )
        if etypefilter and etypefilter.cw_propval("visible"):
            etypefilter.render(w=self.w)
        self.w('<div id="contentmain">\n')
        nav_html = UStringIO()
        if view and not view.handle_pagination:
            view.paginate(w=nav_html.write)
        self.w(nav_html.getvalue())
        view.render(w=self.w)
        self.w(nav_html.getvalue())
        self.w("</div>\n")  # close id=contentmain
        self.w("</div>\n")  # closes id=pageContent
        self.template_footer(view)

    def template_header(
        self, content_type, view=None, page_title="", additional_headers=()
    ):
        page_title = page_title or view.page_title()
        additional_headers = additional_headers or view.html_headers()
        self.template_html_header(content_type, page_title, additional_headers)
        self.template_body_header(view)

    def template_html_header(self, content_type, page_title, additional_headers=()):
        self.write_doctype()
        self._cw.html_headers.define_var("BASE_URL", self._cw.base_url())
        self._cw.html_headers.define_var("DATA_URL", self._cw.datadir_url)
        self.whead(
            '<meta http-equiv="content-type" content="%s; charset=%s"/>\n',
            content_type,
            self._cw.encoding,
        )
        self.whead("\n".join(additional_headers) + "\n")
        self.wview("htmlheader", rset=self.cw_rset)
        if page_title:
            self.whead("<title>%s</title>\n", xml_escape(page_title))

    def template_body_header(self, view):
        self.w("<body>\n")
        self.wview("header", rset=self.cw_rset, view=view)
        self.w('<div id="page"><table width="100%" border="0" id="mainLayout"><tr>\n')
        self.nav_column(view, "left")
        self.w('<td id="contentColumn">\n')
        components = self._cw.vreg["components"]
        rqlcomp = components.select_or_none("rqlinput", self._cw, rset=self.cw_rset)
        if rqlcomp:
            rqlcomp.render(w=self.w, view=view)
        msgcomp = components.select_or_none("applmessages", self._cw, rset=self.cw_rset)
        if msgcomp:
            msgcomp.render(w=self.w)
        self.content_header(view)

    def template_footer(self, view=None):
        self.content_footer(view)
        self.w("</td>\n")
        self.nav_column(view, "right")
        self.w("</tr></table></div>\n")
        self.wview("footer", rset=self.cw_rset, view=view)
        self.w("</body>")

    def nav_column(self, view, context):
        boxes = list(
            self._cw.vreg["ctxcomponents"].poss_visible_objects(
                self._cw, rset=self.cw_rset, view=view, context=context
            )
        )
        if boxes:
            self.w(
                '<td id="navColumn%s"><div class="navboxes">\n', context.capitalize()
            )
            for box in boxes:
                box.render(w=self.w, view=view)
            self.w("</div></td>\n")

    def content_header(self, view=None):
        """by default, display informal messages in content header"""
        self.wview("contentheader", rset=self.cw_rset, view=view)

    def content_footer(self, view=None):
        self.wview("contentfooter", rset=self.cw_rset, view=view)


class ErrorTemplate(TheMainTemplate):
    """fallback template if an internal error occurred during displaying the main
    template. This template may be called for authentication error, which means
    that req.cnx and req.user may not be set.
    """

    __regid__ = "error-template"

    def call(self):
        """display an unexpected error"""
        self.set_request_content_type()
        self._cw.reset_headers()
        view = self._cw.vreg["views"].select("error", self._cw, rset=self.cw_rset)
        self.template_header(
            self.content_type,
            view,
            self._cw._("an error occurred"),
            [NOINDEX, NOFOLLOW],
        )
        view.render(w=self.w)
        self.template_footer(view)

    def template_header(
        self, content_type, view=None, page_title="", additional_headers=()
    ):
        self.write_doctype()
        self.whead(
            '<meta http-equiv="content-type" content="%s; charset=%s"/>\n',
            content_type,
            self._cw.encoding,
        )
        self.whead("\n".join(additional_headers))
        self.wview("htmlheader", rset=self.cw_rset)
        self.w("<title>%s</title>\n", page_title)
        self.w("<body>\n")

    def template_footer(self, view=None):
        self.w("</body>")


class SimpleMainTemplate(TheMainTemplate):

    __regid__ = "main-no-top"

    def template_header(
        self, content_type, view=None, page_title="", additional_headers=()
    ):
        page_title = page_title or view.page_title()
        additional_headers = additional_headers or view.html_headers()
        whead = self.whead
        self.write_doctype()
        whead(
            '<meta http-equiv="content-type" content="%s; charset=%s"/>\n'
            % (content_type, self._cw.encoding)
        )
        whead("\n".join(additional_headers) + "\n")
        self.wview("htmlheader", rset=self.cw_rset)
        whead("<title>%s</title>\n" % xml_escape(page_title))
        self.w("<body>\n")
        self.w('<div id="page">')
        self.w('<table width="100%" border="0" id="mainLayout"><tr>\n')
        self.w('<td id="navColumnLeft">\n')
        self.topleft_header()
        boxes = list(
            self._cw.vreg["ctxcomponents"].poss_visible_objects(
                self._cw, rset=self.cw_rset, view=view, context="left"
            )
        )
        if boxes:
            self.w('<div class="navboxes">\n')
            for box in boxes:
                box.render(w=self.w)
            self.w("</div>\n")
        self.w("</td>")
        self.w('<td id="contentColumn" rowspan="2">')

    def topleft_header(self):
        logo = self._cw.vreg["components"].select_or_none(
            "logo", self._cw, rset=self.cw_rset
        )
        if logo and logo.cw_propval("visible"):
            self.w('<table id="header"><tr>\n')
            self.w("<td>")
            logo.render(w=self.w)
            self.w("</td>\n")
            self.w("</tr></table>\n")


# page parts templates ########################################################


class HTMLHeader(View):
    """default html headers"""

    __regid__ = "htmlheader"

    def call(self, **kwargs):
        self.favicon()
        self.stylesheets()
        self.javascripts()
        self.alternates()

    def favicon(self):
        favicon = self._cw.uiprops.get("FAVICON", None)
        if favicon:
            self.whead('<link rel="shortcut icon" href="%s"/>\n' % favicon)

    def stylesheets(self):
        req = self._cw
        add_css = req.add_css
        for css in req.uiprops["STYLESHEETS"]:
            add_css(css, localfile=False)
        for css in req.uiprops["STYLESHEETS_PRINT"]:
            add_css(css, "print", localfile=False)

    def javascripts(self):
        for jscript in self._cw.uiprops["JAVASCRIPTS"]:
            self._cw.add_js(jscript, localfile=False)

    def alternates(self):
        urlgetter = self._cw.vreg["components"].select_or_none(
            "rss_feed_url", self._cw, rset=self.cw_rset
        )
        if urlgetter is not None:
            self.whead(
                '<link rel="alternate" type="application/rss+xml" title="RSS feed" href="%s"/>\n'
                % xml_escape(urlgetter.feed_url())
            )
        if self.cw_rset and len(self.cw_rset) == 1:
            for mimetype in RDF_MIMETYPE_TO_FORMAT:
                try:
                    self.whead(
                        f'<link rel="alternate" type="{mimetype}" title="{mimetype}" href="{self._cw.base_url()}{self.cw_rset.one().rest_path()}"/>\n'
                    )
                except NotAnEntity:
                    # was a string, or a number (but not an eid)
                    continue


class HTMLPageHeader(View):
    """default html page header"""

    __regid__ = "header"
    main_cell_components = ("appliname", "breadcrumbs")
    headers = (
        ("headtext", "header-left"),
        ("header-center", "header-center"),
        ("header-right", "header-right"),
    )

    def call(self, view, **kwargs):
        self.main_header(view)
        self.w('<div id="stateheader">')
        self.state_header()
        self.w("</div>")

    def main_header(self, view):
        """build the top menu with authentification info and the rql box"""
        self.w('<table id="header"><tr>\n')
        for colid, context in self.headers:
            self.w('<td id="%s">', colid)
            components = self._cw.vreg["ctxcomponents"].poss_visible_objects(
                self._cw, rset=self.cw_rset, view=view, context=context
            )
            for comp in components:
                comp.render(w=self.w)
                self.w("&#160;")
            self.w("</td>")
        self.w("</tr></table>\n")

    def state_header(self):
        state = self._cw.search_state
        if state[0] == "normal":
            return
        _ = self._cw._
        value = self._cw.view("oneline", self._cw.eid_rset(state[1][1]))
        msg = " ".join(
            (
                _("searching for"),
                display_name(self._cw, state[1][3]),
                _("to associate with"),
                value,
                _("by relation"),
                '"',
                display_name(self._cw, state[1][2], state[1][0]),
                '"',
            )
        )
        return self.w('<div class="stateMessage">%s</div>', msg)


class HTMLPageFooter(View):
    """default html page footer: include footer actions"""

    __regid__ = "footer"

    def call(self, **kwargs):
        self.w('<div id="footer">')
        self.footer_content()
        self.w("</div>")

    def footer_content(self):
        actions = self._cw.vreg["actions"].possible_actions(
            self._cw, rset=self.cw_rset, view=self.cw_extra_kwargs["view"]
        )
        footeractions = actions.get("footer", ())
        for i, action in enumerate(footeractions):
            self.w('<a href="%s">%s</a>', action.url(), self._cw._(action.title))
            if i < (len(footeractions) - 1):
                self.w(" | ")


class HTMLContentHeader(View):
    """default html page content header: include selectable content navigation components"""

    __regid__ = "contentheader"

    def call(self, view, **kwargs):
        """by default, display informal messages in content header"""
        components = self._cw.vreg["ctxcomponents"].poss_visible_objects(
            self._cw, rset=self.cw_rset, view=view, context="navtop"
        )
        if components:
            self.w('<div id="contentheader">')
            for comp in components:
                comp.render(w=self.w, view=view)
            self.w('</div><div class="clear"></div>')


class HTMLContentFooter(View):
    """default html page content footer: include selectable content navigation
    components
    """

    __regid__ = "contentfooter"

    def call(self, view, **kwargs):
        components = self._cw.vreg["ctxcomponents"].poss_visible_objects(
            self._cw, rset=self.cw_rset, view=view, context="navbottom"
        )
        if components:
            self.w('<div id="contentfooter">')
            for comp in components:
                comp.render(w=self.w, view=view)
            self.w("</div>")


class BaseLogForm(forms.FieldsForm):
    """Abstract Base login form to be used by any login form"""

    __abstract__ = True

    __regid__ = "logform"
    domid = "loginForm"
    needs_css = ("cubicweb.login.css",)

    onclick_base = "javascript: cw.htmlhelpers.popupLoginBox('%s', '%s');"
    onclick_args = (None, None)

    @classproperty
    def form_buttons(cls):
        # we use a property because sub class will need to define their own onclick_args.
        # Therefor we can't juste make the string formating when instanciating this class
        onclick = cls.onclick_base % cls.onclick_args
        form_buttons = [
            fw.SubmitButton(label=_("log in"), attrs={"class": "loginButton"}),
            fw.ResetButton(
                label=_("cancel"), attrs={"class": "loginButton", "onclick": onclick}
            ),
        ]
        # Can't shortcut next access because __dict__ is a "dictproxy" which
        # does not support items assignement.
        # cls.__dict__['form_buttons'] = form_buttons
        return form_buttons

    def form_action(self):
        if self.action is None:
            # reuse existing redirection if it exists
            target = self._cw.form.get("postlogin_path", self._cw.relative_path())
            url_args = {}
            if target and target != "/":
                url_args["postlogin_path"] = target
            return self._cw.build_url("login", **url_args)
        return super().form_action()


class LogForm(BaseLogForm):
    """Simple login form that send username and password"""

    __regid__ = "logform"
    domid = "loginForm"
    needs_css = ("cubicweb.login.css",)
    # XXX have to recall fields name since python is mangling __login/__password
    __login = ff.StringField("__login", widget=fw.TextInput({"class": "data"}))
    __password = ff.StringField(
        "__password",
        label=_("password"),
        widget=fw.PasswordSingleInput({"class": "data"}),
    )

    onclick_args = ("popupLoginBox", "__login")


class LogFormView(View):
    # XXX an awful lot of hardcoded assumptions there
    #     makes it unobvious to reuse/specialize
    __regid__ = "logform"
    __select__ = match_kwargs("id", "klass")

    title = "log in"

    def call(self, id, klass, title=True, showmessage=True):
        self.w('<div id="%s" class="%s">', id, klass)
        if title:
            stitle = self._cw.property_value("ui.site-title")
            if stitle:
                stitle = xml_escape(stitle)
            else:
                stitle = "&#160;"
            self.w('<div class="loginTitle">%s</div>', stitle)
        self.w('<div class="loginContent">\n')
        # don't call self._cw.message twice since it pops the id
        message = self._cw.message
        if showmessage and message:
            self.w('<div class="loginMessage">%s</div>\n', message)
        config = self._cw.vreg.config
        if config["auth-mode"] != "http":
            self.login_form(id)  # Cookie authentication
        self.w("</div>")
        self.w("</div>\n")

    def login_form(self, id):
        cw = self._cw
        form = cw.vreg["forms"].select("logform", cw)
        if cw.vreg.config["allow-email-login"]:
            label = cw._("login or email")
        else:
            label = cw.pgettext("CWUser", "login")
        form.field_by_name("__login").label = label
        form.render(w=self.w, table_class="", display_progress_div=False)
        cw.html_headers.add_onload('jQuery("#__login:visible").focus()')


LogFormTemplate = class_renamed("LogFormTemplate", LogFormView)
