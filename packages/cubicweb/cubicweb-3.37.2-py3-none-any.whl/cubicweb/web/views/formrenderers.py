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
"""
Renderers
---------

.. Note::
   Form renderers are responsible to layout a form to HTML.

Here are the base renderers available:

.. autoclass:: cubicweb.web.views.formrenderers.FormRenderer
.. autoclass:: cubicweb.web.views.formrenderers.HTableFormRenderer
.. autoclass:: cubicweb.web.views.formrenderers.EntityCompositeFormRenderer
.. autoclass:: cubicweb.web.views.formrenderers.EntityFormRenderer
.. autoclass:: cubicweb.web.views.formrenderers.EntityInlinedFormRenderer

"""


from logilab.common.registry import yes
from logilab.mtconverter import xml_escape

from cubicweb import _
from cubicweb import tags, uilib
from cubicweb.appobject import AppObject
from cubicweb.predicates import is_instance
from cubicweb.uilib import eid_param
from cubicweb.utils import json_dumps
from cubicweb.web import formwidgets as fwdgs


def checkbox(name, value, attrs="", checked=None):
    if checked is None:
        checked = value
    checked = checked and 'checked="checked"' or ""
    return '<input type="checkbox" name="{}" value="{}" {} {} />'.format(
        name,
        value,
        checked,
        attrs,
    )


def field_label(form, field):
    if callable(field.label):
        return field.label(form, field)
    # XXX with 3.6 we can now properly rely on 'if field.role is not None' and
    # stop having a tuple for label
    if isinstance(field.label, tuple):  # i.e. needs contextual translation
        return form._cw.pgettext(*field.label)
    return form._cw._(field.label)


class FormRenderer(AppObject):
    """This is the 'default' renderer, displaying fields in a two columns table:

    +--------------+--------------+
    | field1 label | field1 input |
    +--------------+--------------+
    | field2 label | field2 input |
    +--------------+--------------+

    +---------+
    | buttons |
    +---------+
    """

    __registry__ = "formrenderers"
    __regid__ = "default"

    _options = (
        "display_label",
        "display_help",
        "display_progress_div",
        "table_class",
        "button_bar_class",
        # add entity since it may be given to select the renderer
        "entity",
    )
    display_label = True
    display_help = True
    display_progress_div = True
    table_class = "attributeForm"
    button_bar_class = "formButtonBar"

    def __init__(self, req=None, rset=None, row=None, col=None, **kwargs):
        super().__init__(req, rset=rset, row=row, col=col)
        if self._set_options(kwargs):
            raise ValueError("unconsumed arguments %s" % kwargs)

    def _set_options(self, kwargs):
        for key in self._options:
            try:
                setattr(self, key, kwargs.pop(key))
            except KeyError:
                continue
        return kwargs

    # renderer interface ######################################################

    def render(self, w, form, values):
        self._set_options(values)
        form.add_media()
        data = []
        _w = data.append
        _w(self.open_form(form, values))
        self.render_content(_w, form, values)
        _w(self.close_form(form, values))
        errormsg = self.error_message(form)
        if errormsg:
            data.insert(0, errormsg)
        # NOTE: we call str because `tag` objects may be found within data
        #       e.g. from the cwtags library
        w("".join(str(x) for x in data))

    def render_content(self, w, form, values):
        if self.display_progress_div:
            w('<div id="progress">%s</div>' % self._cw._("validating..."))
        w("\n<fieldset>\n")
        self.render_fields(w, form, values)
        self.render_buttons(w, form)
        w("\n</fieldset>\n")

    def render_label(self, form, field):
        if field.label is None:
            return ""
        label = field_label(form, field)
        attrs = {"for": field.dom_id(form)}
        if field.required:
            attrs["class"] = "required"
        return tags.label(label, **attrs)

    def render_help(self, form, field):
        help = []
        descr = field.help
        if callable(descr):
            descr = descr(form, field)
        if descr:
            help.append('<div class="helper">%s</div>' % self._cw._(descr))
        example = field.example_format(self._cw)
        if example:
            help.append(
                '<div class="helper">(%s: %s)</div>'
                % (self._cw._("sample format"), example)
            )
        return "&#160;".join(help)

    # specific methods (mostly to ease overriding) #############################

    def error_message(self, form):
        """return formatted error message

        This method should be called once inlined field errors has been consumed
        """
        req = self._cw
        errex = form.form_valerror
        # get extra errors
        if errex is not None:
            errormsg = req._("please correct the following errors:")
            errors = form.remaining_errors()
            if errors:
                if len(errors) > 1:
                    templstr = "<li>%s</li>\n"
                else:
                    templstr = "&#160;%s\n"
                for field, err in errors:
                    if not field:
                        errormsg += templstr % err
                    else:
                        errormsg += templstr % "%s: %s" % (req._(field), err)
                if len(errors) > 1:
                    errormsg = "<ul>%s</ul>" % errormsg
            return '<div class="errorMessage">%s</div>' % errormsg
        return ""

    def open_form(self, form, values, **attrs):
        if form.needs_multipart:
            enctype = "multipart/form-data"
        else:
            enctype = "application/x-www-form-urlencoded"
        attrs.setdefault("enctype", enctype)
        attrs.setdefault("method", "post")
        attrs.setdefault("action", form.form_action() or "#")
        if form.domid:
            attrs.setdefault("id", form.domid)
        if form.onsubmit:
            attrs.setdefault("onsubmit", form.onsubmit)
        if form.cssstyle:
            attrs.setdefault("style", form.cssstyle)
        if form.cssclass:
            attrs.setdefault("class", form.cssclass)
        if form.cwtarget:
            attrs.setdefault("target", form.cwtarget)
        if not form.autocomplete:
            attrs.setdefault("autocomplete", "off")
        return "<form %s>" % uilib.sgml_attributes(attrs)

    def close_form(self, form, values):
        """seems dumb but important for consistency w/ close form, and necessary
        for form renderers overriding open_form to use something else or more than
        and <form>
        """
        out = "</form>"
        if form.cwtarget:
            attrs = {
                "name": form.cwtarget,
                "id": form.cwtarget,
                "width": "0px",
                "height": "0px",
                "src": "javascript: void(0);",
            }
            out = ("<iframe %s></iframe>\n" % uilib.sgml_attributes(attrs)) + out
        return out

    def render_fields(self, w, form, values):
        fields = self._render_hidden_fields(w, form)
        if fields:
            self._render_fields(fields, w, form)
        self.render_child_forms(w, form, values)

    def render_child_forms(self, w, form, values):
        # render
        for childform in getattr(form, "forms", []):
            self.render_fields(w, childform, values)

    def _render_hidden_fields(self, w, form):
        fields = form.fields[:]
        for field in form.fields:
            if not field.is_visible():
                w(field.render(form, self))
                w("\n")
                fields.remove(field)
        return fields

    def _render_fields(self, fields, w, form):
        byfieldset = {}
        for field in fields:
            byfieldset.setdefault(field.fieldset, []).append(field)
        if form.fieldsets_in_order:
            fieldsets = form.fieldsets_in_order
        else:
            fieldsets = byfieldset
        for fieldset in list(fieldsets):
            try:
                fields = byfieldset.pop(fieldset)
            except KeyError:
                self.warning("no such fieldset: %s (%s)", fieldset, form)
                continue
            w("<fieldset>\n")
            if fieldset:
                w("<legend>%s</legend>" % self._cw.__(fieldset))
            w('<table class="%s">\n' % self.table_class)
            for field in fields:
                w(f'<tr class="{field.name}_{field.role}_row">\n')
                if self.display_label and field.label is not None:
                    w('<th class="labelCol">%s</th>\n' % self.render_label(form, field))
                w("<td")
                if field.label is None:
                    w(' colspan="2"')
                error = form.field_error(field)
                if error:
                    w(' class="error"')
                w(">\n")
                w(field.render(form, self))
                w("\n")
                if error:
                    self.render_error(w, error)
                if self.display_help:
                    w(self.render_help(form, field))
                w("</td></tr>\n")
            w("</table></fieldset>\n")
        if byfieldset:
            self.warning("unused fieldsets: %s", ", ".join(byfieldset))

    def render_buttons(self, w, form):
        if not form.form_buttons:
            return
        w('<table class="%s">\n<tr>\n' % self.button_bar_class)
        for button in form.form_buttons:
            w("<td>%s</td>\n" % button.render(form))
        w("</tr></table>")

    def render_error(self, w, err):
        """return validation error for widget's field, if any"""
        w('<span class="errorMsg">%s</span>' % err)


class BaseFormRenderer(FormRenderer):
    """use form_renderer_id = 'base' if you want base FormRenderer layout even
    when selected for an entity
    """

    __regid__ = "base"


class HTableFormRenderer(FormRenderer):
    """The 'htable' form renderer display fields horizontally in a table:

    +--------------+--------------+---------+
    | field1 label | field2 label |         |
    +--------------+--------------+---------+
    | field1 input | field2 input | buttons |
    +--------------+--------------+---------+
    """

    __regid__ = "htable"

    display_help = False

    def _render_fields(self, fields, w, form):
        w('<table border="0" class="htableForm">')
        if self.display_label:
            w("<tr>")
            for field in fields:
                w('<th class="labelCol">%s</th>' % self.render_label(form, field))
                if self.display_help:
                    w(self.render_help(form, field))
            # empty slot for buttons
            w('<th class="labelCol">&#160;</th>')
            w("</tr>")
        w("<tr>")
        for field in fields:
            error = form.field_error(field)
            if error:
                w('<td class="error">')
                self.render_error(w, error)
            else:
                w("<td>")
            w(field.render(form, self))
            w("</td>")
        w("<td>")
        for button in form.form_buttons:
            w(button.render(form))
        w("</td>")
        w("</tr>")
        w("</table>")

    def render_buttons(self, w, form):
        pass


class OneRowTableFormRenderer(FormRenderer):
    """The 'htable' form renderer display fields horizontally in a table:

    +--------------+--------------+--------------+--------------+---------+
    | field1 label | field1 input | field2 label | field2 input | buttons |
    +--------------+--------------+--------------+--------------+---------+
    """

    __regid__ = "onerowtable"

    display_help = False

    def _render_fields(self, fields, w, form):
        w('<table border="0" class="oneRowTableForm">')
        w("<tr>")
        for field in fields:
            if self.display_label:
                w('<th class="labelCol">%s</th>' % self.render_label(form, field))
            if self.display_help:
                w(self.render_help(form, field))
            error = form.field_error(field)
            if error:
                w('<td class="error">')
                self.render_error(w, error)
            else:
                w("<td>")
            w(field.render(form, self))
            w("</td>")
        w("<td>")
        for button in form.form_buttons:
            w(button.render(form))
        w("</td>")
        w("</tr>")
        w("</table>")

    def render_buttons(self, w, form):
        pass


class EntityCompositeFormRenderer(FormRenderer):
    """This is a specific renderer for the multiple entities edition form
    ('muledit').

    Each entity form will be displayed in row off a table, with a check box for
    each entities to indicate which ones are edited. Those checkboxes should be
    automatically updated when something is edited.
    """

    __regid__ = "composite"

    _main_display_fields = None

    def render_fields(self, w, form, values):
        if form.parent_form is None:
            w('<table class="listing">')
            # get fields from the first subform with something to display (we
            # may have subforms with nothing editable that will simply be
            # skipped later)
            for subform in form.forms:
                subfields = [field for field in subform.fields if field.is_visible()]
                if subfields:
                    break
            if subfields:
                # main form, display table headers
                w('<tr class="header">')
                w(
                    '<th align="left">%s</th>'
                    % tags.input(
                        type="checkbox",
                        title=self._cw._("toggle check boxes"),
                        onclick="setCheckboxesState('eid', null, this.checked)",
                    )
                )
                for field in subfields:
                    w("<th>%s</th>" % field_label(form, field))
                w("</tr>")
        super().render_fields(w, form, values)
        if form.parent_form is None:
            w("</table>")
            if self._main_display_fields:
                super()._render_fields(self._main_display_fields, w, form)

    def _render_fields(self, fields, w, form):
        if form.parent_form is not None:
            entity = form.edited_entity
            values = form.form_previous_values
            qeid = eid_param("eid", entity.eid)
            cbsetstate = "setCheckboxesState('eid', %s, 'checked')" % xml_escape(
                json_dumps(entity.eid)
            )
            w('<tr class="%s">' % (entity.cw_row % 2 and "even" or "odd"))
            # XXX turn this into a widget used on the eid field
            w("<td>%s</td>" % checkbox("eid", entity.eid, checked=qeid in values))
            for field in fields:
                error = form.field_error(field)
                if error:
                    w('<td class="error">')
                    self.render_error(w, error)
                else:
                    w("<td>")
                if isinstance(
                    field.widget, (fwdgs.Select, fwdgs.CheckBox, fwdgs.Radio)
                ):
                    field.widget.attrs["onchange"] = cbsetstate
                elif isinstance(field.widget, fwdgs.Input):
                    field.widget.attrs["onkeypress"] = cbsetstate
                # XXX else
                w("<div>%s</div>" % field.render(form, self))
                w("</td>\n")
            w("</tr>")
        else:
            self._main_display_fields = fields


class EntityFormRenderer(BaseFormRenderer):
    """This is the 'default' renderer for entity's form.

    You can still use form_renderer_id = 'base' if you want base FormRenderer
    layout even when selected for an entity.
    """

    __regid__ = "default"
    # needs some additional points in some case (XXX explain cases)
    __select__ = is_instance("Any") & yes()

    _options = FormRenderer._options + ("main_form_title",)
    main_form_title = _("main informations")

    def open_form(self, form, values):
        attrs_fs_label = ""
        if self.main_form_title:
            attrs_fs_label += (
                '<div class="iformTitle"><span>%s</span></div>'
                % self._cw._(self.main_form_title)
            )
        attrs_fs_label += '<div class="formBody">'
        return attrs_fs_label + super().open_form(form, values)

    def close_form(self, form, values):
        """seems dumb but important for consistency w/ close form, and necessary
        for form renderers overriding open_form to use something else or more than
        and <form>
        """
        return super().close_form(form, values) + "</div>"

    def render_buttons(self, w, form):
        if len(form.form_buttons) == 3:
            w(
                """<table width="100%%">
  <tbody>
   <tr><td align="center">
     %s
   </td><td style="align: right; width: 50%%;">
     %s
     %s
   </td></tr>
  </tbody>
 </table>"""
                % tuple(button.render(form) for button in form.form_buttons)
            )
        else:
            super().render_buttons(w, form)


class EntityInlinedFormRenderer(EntityFormRenderer):
    """This is a specific renderer for entity's form inlined into another
    entity's form.
    """

    __regid__ = "inline"
    fieldset_css_class = "subentity"

    def render_title(self, w, form, values):
        w('<div class="iformTitle">')
        w(
            "<span>%(title)s</span> "
            '#<span class="icounter">%(counter)s</span> ' % values
        )
        if values["removejs"]:
            values["removemsg"] = self._cw._("remove-inlined-entity-form")
            w(
                '[<a href="javascript: %(removejs)s;$.noop();">%(removemsg)s</a>]'
                % values
            )
        w("</div>")

    def render(self, w, form, values):
        form.add_media()
        self.open_form(w, form, values)
        self.render_title(w, form, values)
        # XXX that stinks
        # cleanup values
        for key in ("title", "removejs", "removemsg"):
            values.pop(key, None)
        self.render_fields(w, form, values)
        self.close_form(w, form, values)

    def open_form(self, w, form, values):
        try:
            w('<div id="div-%(divid)s" onclick="%(divonclick)s">' % values)
        except KeyError:
            w('<div id="div-%(divid)s">' % values)
        else:
            w(
                '<div id="notice-%s" class="notice">%s</div>'
                % (
                    values["divid"],
                    self._cw._("click on the box to cancel the deletion"),
                )
            )
        w('<div class="iformBody">')

    def close_form(self, w, form, values):
        w("</div></div>")

    def render_fields(self, w, form, values):
        w('<fieldset id="fs-%(divid)s">' % values)
        fields = self._render_hidden_fields(w, form)
        w("</fieldset>")
        w('<fieldset class="%s">' % self.fieldset_css_class)
        if fields:
            self._render_fields(fields, w, form)
        self.render_child_forms(w, form, values)
        w("</fieldset>")
