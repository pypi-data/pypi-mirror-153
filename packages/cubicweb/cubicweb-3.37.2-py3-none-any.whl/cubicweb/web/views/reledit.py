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
"""edit entity attributes/relations from any view, without going to the entity
form
"""


import copy

from logilab.common.decorators import cached
from logilab.mtconverter import xml_escape

from cubicweb import _
from cubicweb import neg_role
from cubicweb.predicates import non_final_entity, match_kwargs
from cubicweb.schema import display_name
from cubicweb.utils import json, json_dumps
from cubicweb.view import EntityView
from cubicweb.web import stdmsgs
from cubicweb.web.formwidgets import Button, SubmitButton
from cubicweb.web.views.ajaxcontroller import ajaxfunc


class _DummyForm(object):
    __slots__ = ("event_args",)

    def form_render(self, **_args):
        return ""

    def render(self, *_args, **_kwargs):
        return ""

    def append_field(self, *args):
        pass

    def add_hidden(self, *args):
        pass


class AutoClickAndEditFormView(EntityView):
    __regid__ = "reledit"
    __select__ = non_final_entity() & match_kwargs("rtype")

    # ui side continuations
    _onclick = (
        "cw.reledit.loadInlineEditionForm('%(formid)s', %(eid)s, '%(rtype)s', '%(role)s', "
        "'%(divid)s', %(reload)s, '%(vid)s', '%(action)s');"
    )
    _cancelclick = "cw.reledit.cleanupAfterCancel('%s')"

    # ui side actions/buttons
    _addzone = '<img title="%(msg)s" src="%(logo)s" alt="%(msg)s"/>'
    _addmsg = _("click to add a value")
    _addlogo = "plus.png"
    _deletezone = '<img title="%(msg)s" src="%(logo)s" alt="%(msg)s"/>'
    _deletemsg = _("click to delete this value")
    _deletelogo = "cancel.png"
    _editzone = '<img title="%(msg)s" src="%(logo)s" alt="%(msg)s"/>'
    _editzonemsg = _("click to edit this field")
    _editlogo = "pen_icon.png"

    # renderer
    _form_renderer_id = "base"

    def entity_call(
        self,
        entity,
        rtype=None,
        role="subject",
        reload=False,  # controls reloading the whole page after change
        # boolean, eid (to redirect), or
        # function taking the subject entity & returning a boolean or an eid
        rvid=None,  # vid to be applied to other side of rtype (non final relations only)
        default_value=None,
        formid="base",
        action=None,
    ):
        """display field to edit entity's `rtype` relation on click"""
        assert rtype
        self._cw.add_css("cubicweb.form.css")
        self._cw.add_js(
            ("cubicweb.reledit.js", "cubicweb.edition.js", "cubicweb.ajax.js")
        )
        self.entity = entity
        rschema = self._cw.vreg.schema[rtype]
        rctrl = self._cw.vreg["uicfg"].select("reledit", self._cw, entity=entity)
        self._rules = rctrl.etype_get(
            self.entity.e_schema.type, rschema.type, role, "*"
        )
        reload = self._compute_reload(rschema, role, reload)
        divid = self._build_divid(rtype, role, self.entity.eid)
        if rschema.final:
            self._handle_attribute(rschema, role, divid, reload, action)
        else:
            if self._is_composite():
                self._handle_composite(rschema, role, divid, reload, formid, action)
            else:
                self._handle_relation(rschema, role, divid, reload, formid, action)

    def _handle_attribute(self, rschema, role, divid, reload, action):
        rvid = self._rules.get("rvid", None)
        if rvid is not None:
            value = self._cw.view(
                rvid, entity=self.entity, rtype=rschema.type, role=role
            )
        else:
            value = self.entity.printable_value(rschema.type)
        if not self._should_edit_attribute(rschema):
            self.w(value)
            return
        form, renderer = self._build_form(
            self.entity, rschema, role, divid, "base", reload, action
        )
        value = value or self._compute_default_value(rschema, role)
        self.view_form(divid, value, form, renderer)

    def _compute_formid_value(self, rschema, role, rvid, formid):
        related_rset = self.entity.related(rschema.type, role)
        if related_rset:
            value = self._cw.view(rvid, related_rset)
        else:
            value = self._compute_default_value(rschema, role)
        if not self._should_edit_relation(rschema, role):
            return None, value
        return formid, value

    def _handle_relation(self, rschema, role, divid, reload, formid, action):
        rvid = self._rules.get("rvid", "autolimited")
        formid, value = self._compute_formid_value(rschema, role, rvid, formid)
        if formid is None:
            return self.w(value)
        form, renderer = self._build_form(
            self.entity, rschema, role, divid, formid, reload, action, dict(vid=rvid)
        )
        self.view_form(divid, value, form, renderer)

    def _handle_composite(self, rschema, role, divid, reload, formid, action):
        # this is for attribute-like composites (1 target type, 1 related entity at most, for now)
        entity = self.entity
        related_rset = entity.related(rschema.type, role)
        add_related = self._may_add_related(related_rset, rschema, role)
        edit_related = self._may_edit_related_entity(related_rset, rschema, role)
        delete_related = edit_related and self._may_delete_related(
            related_rset, rschema, role
        )
        rvid = self._rules.get("rvid", "autolimited")
        formid, value = self._compute_formid_value(rschema, role, rvid, formid)
        if formid is None or not (edit_related or add_related):
            # till we learn to handle cases where not (edit_related or add_related)
            self.w(value)
            return
        form, renderer = self._build_form(
            entity, rschema, role, divid, formid, reload, action, dict(vid=rvid)
        )
        self.view_form(
            divid, value, form, renderer, edit_related, add_related, delete_related
        )

    @cached
    def _compute_ttypes(self, rschema, role):
        dual_role = neg_role(role)
        return getattr(rschema, "%ss" % dual_role)(self.entity.e_schema)

    def _compute_reload(self, rschema, role, reload):
        ctrl_reload = self._rules.get("reload", reload)
        if callable(ctrl_reload):
            ctrl_reload = ctrl_reload(self.entity)
        if isinstance(ctrl_reload, int) and ctrl_reload > 1:  # not True/False
            ctrl_reload = self._cw.build_url(ctrl_reload)
        return ctrl_reload

    def _compute_default_value(self, rschema, role):
        default = self._rules.get("novalue_label")
        if default is None:
            if self._rules.get("novalue_include_rtype"):
                default = self._cw._("<%s not specified>") % display_name(
                    self._cw, rschema.type, role
                )
            else:
                default = self._cw._("<not specified>")
        else:
            default = self._cw._(default)
        return xml_escape(default)

    def _is_composite(self):
        return self._rules.get("edit_target") == "related"

    def _may_add_related(self, related_rset, rschema, role):
        """ok for attribute-like composite entities"""
        ttypes = self._compute_ttypes(rschema, role)
        if len(ttypes) > 1:  # many etypes: learn how to do it
            return False
        rdef = rschema.role_relation_definition(self.entity.e_schema, ttypes[0], role)
        card = rdef.role_cardinality(role)
        if related_rset or card not in "?1":
            return False
        if role == "subject":
            kwargs = {"fromeid": self.entity.eid}
        else:
            kwargs = {"toeid": self.entity.eid}
        return rdef.has_perm(self._cw, "add", **kwargs)

    def _may_edit_related_entity(self, related_rset, rschema, role):
        """controls the edition of the related entity"""
        ttypes = self._compute_ttypes(rschema, role)
        if len(ttypes) > 1 or len(related_rset.rows) != 1:
            return False
        if (
            self.entity.e_schema.relation_definition(rschema, role).role_cardinality(
                role
            )
            not in "?1"
        ):
            return False
        return related_rset.get_entity(0, 0).cw_has_perm("update")

    def _may_delete_related(self, related_rset, rschema, role):
        # we assume may_edit_related, only 1 related entity
        if not related_rset:
            return False
        rentity = related_rset.get_entity(0, 0)
        entity = self.entity
        if role == "subject":
            kwargs = {"fromeid": entity.eid, "toeid": rentity.eid}
            cardinality = rschema.relation_definitions[
                (entity.cw_etype, rentity.cw_etype)
            ].cardinality[0]
        else:
            kwargs = {"fromeid": rentity.eid, "toeid": entity.eid}
            cardinality = rschema.rdefs[
                (rentity.cw_etype, entity.cw_etype)
            ].cardinality[1]
        if cardinality in "1+":
            return False
        # NOTE: should be sufficient given a well built schema/security
        return rschema.has_perm(self._cw, "delete", **kwargs)

    def _build_zone(self, zonedef, msg, logo):
        return zonedef % {
            "msg": xml_escape(self._cw._(msg)),
            "logo": xml_escape(self._cw.data_url(logo)),
        }

    def _build_edit_zone(self):
        return self._build_zone(self._editzone, self._editzonemsg, self._editlogo)

    def _build_delete_zone(self):
        return self._build_zone(self._deletezone, self._deletemsg, self._deletelogo)

    def _build_add_zone(self):
        return self._build_zone(self._addzone, self._addmsg, self._addlogo)

    def _build_divid(self, rtype, role, entity_eid):
        """builds an id for the root div of a reledit widget"""
        return "%s-%s-%s" % (rtype, role, entity_eid)

    def _build_args(self, entity, rtype, role, formid, reload, action, extradata=None):
        divid = self._build_divid(rtype, role, entity.eid)
        event_args = {
            "divid": divid,
            "eid": entity.eid,
            "rtype": rtype,
            "formid": formid,
            "reload": json_dumps(reload),
            "action": action,
            "role": role,
            "vid": "",
        }
        if extradata:
            event_args.update(extradata)
        return event_args

    def _prepare_form(self, entity, rschema, role, action):
        assert action in ("edit_rtype", "edit_related", "add", "delete"), action
        if action == "edit_rtype":
            return False, entity
        label = True
        if action in ("edit_related", "delete"):
            edit_entity = entity.related(rschema, role).get_entity(0, 0)
        elif action == "add":
            add_etype = self._compute_ttypes(rschema, role)[0]
            _new_entity = self._cw.vreg["etypes"].etype_class(add_etype)(self._cw)
            _new_entity.eid = next(self._cw.varmaker)
            edit_entity = _new_entity
            # XXX see forms.py ~ 276 and entities.linked_to method
            #     is there another way?
            self._cw.form["__linkto"] = "%s:%s:%s" % (
                rschema,
                entity.eid,
                neg_role(role),
            )
        assert edit_entity
        return label, edit_entity

    def _build_renderer(self, related_entity, display_label):
        return self._cw.vreg["formrenderers"].select(
            self._form_renderer_id,
            self._cw,
            entity=related_entity,
            display_label=display_label,
            table_class="attributeForm" if display_label else "",
            display_help=False,
            button_bar_class="buttonbar",
            display_progress_div=False,
        )

    def _build_form(
        self,
        entity,
        rschema,
        role,
        divid,
        formid,
        reload,
        action,
        extradata=None,
        **formargs,
    ):
        rtype = rschema.type
        event_args = self._build_args(
            entity, rtype, role, formid, reload, action, extradata
        )
        if not action:
            form = _DummyForm()
            form.event_args = event_args
            return form, None
        label, edit_entity = self._prepare_form(entity, rschema, role, action)
        cancelclick = self._cancelclick % divid
        form = self._cw.vreg["forms"].select(
            formid,
            self._cw,
            rset=edit_entity.as_rset(),
            entity=edit_entity,
            domid="%s-form" % divid,
            formtype="inlined",
            action=self._cw.build_url(
                "validateform", __onsuccess="window.parent.cw.reledit.onSuccess"
            ),
            cwtarget="eformframe",
            cssclass="releditForm",
            **formargs,
        )
        # pass reledit arguments
        for pname, pvalue in event_args.items():
            form.add_hidden("__reledit|" + pname, pvalue)
        # handle buttons
        if form.form_buttons:  # edition, delete
            form_buttons = []
            for button in form.form_buttons:
                if not button.label.endswith("apply"):
                    if button.label.endswith("cancel"):
                        button = copy.deepcopy(button)
                        button.cwaction = None
                        button.onclick = cancelclick
                        if "class" in button.attrs:
                            new_class = button.attrs["class"].replace(
                                "cwjs-edition-cancel", ""
                            )
                            button.attrs["class"] = new_class
                    form_buttons.append(button)
            form.form_buttons = form_buttons
        else:  # base
            form.form_buttons = [
                SubmitButton(),
                Button(stdmsgs.BUTTON_CANCEL, onclick=cancelclick),
            ]
        form.event_args = event_args
        if formid == "base":
            field = form.field_by_name(rtype, role, entity.e_schema)
            form.append_field(field)
        return form, self._build_renderer(edit_entity, label)

    def _should_edit_attribute(self, rschema):
        entity = self.entity
        rdef = entity.e_schema.relation_definition(rschema)
        # check permissions
        if not entity.cw_has_perm("update"):
            return False
        rdef = entity.e_schema.relation_definition(rschema)
        return rdef.has_perm(self._cw, "update", eid=entity.eid)

    def _may_delete_related_entities(self, related_rset, rschema, ttypes, role):
        rdef = rschema.role_relation_definition(self.entity.e_schema, ttypes[0], role)
        if role == "subject":
            # on relation with cardinality 1 or ?, we need delete perm as well
            # if the relation is already set
            if rdef.role_cardinality(role) in "1?" and not any(
                rdef.has_perm(self._cw, "delete", fromeid=self.entity.eid, toeid=row[0])
                for row in related_rset
            ):
                return False
        elif role == "object":
            # on relation with cardinality 1 or ?, we need delete perm as well
            # if the relation is already set
            if rdef.role_cardinality(role) in "1?" and not any(
                rdef.has_perm(self._cw, "delete", toeid=self.entity.eid, fromeid=row[0])
                for row in related_rset
            ):
                return False
        return True

    def _has_unrelated_entities_to_add(self, rschema, ttypes, role, **perm_args):
        """can add at least one unrelated entity"""
        for target in ttypes:
            if self.entity.unrelated(rschema, target, role, limit=1):
                return True
        return False

    def _should_edit_relation(self, rschema, role):
        """reledit for an relation if one of following conditions is satisfied:
        * the relation dont have rqlexpr permissions and can be deleted
        * at least one of related entites can be deleted

        These two conditions are consistent with thoses in
        AutoformSectionRelationTags.relations_by_section.

        We also check that at least one unrelated entity exists and can be added

        """

        eeid = self.entity.eid
        perm_args = {"fromeid": eeid} if role == "subject" else {"toeid": eeid}
        ttypes = self._compute_ttypes(rschema, role)
        # check permission which are not rqlexprs
        for target in ttypes:
            rdef = rschema.role_relation_definition(self.entity.e_schema, target, role)
            if rdef.has_perm(self._cw, "add", **perm_args):
                return True
        # can delete related entities
        related_rset = self.entity.related(rschema.type, role)
        if related_rset:
            if not self._may_delete_related_entities(
                related_rset, rschema, ttypes, role
            ):
                return False
            return True
        # there are unrelated entities to be added
        if self._has_unrelated_entities_to_add(rschema, ttypes, role, **perm_args):
            return True
        # no related or unrelated entities exist
        # consider autoform_permissions_overrides
        permsoverrides = self._cw.vreg["uicfg"].select(
            "autoform_permissions_overrides", self._cw, entity=self.entity
        )
        if "add_on_new" in permsoverrides.etype_get(
            self.entity.e_schema, rschema, role
        ):
            return True
        # there no way to verify subject/object related permissions as no unrelated
        # entities exist. In doubt we dont display the reledit for security reasons
        return False

    def _open_form_wrapper(
        self, divid, value, form, renderer, _edit_related, _add_related, _delete_related
    ):
        self.w(
            '<div id="%(id)s-reledit" onmouseout="%(out)s" onmouseover="%(over)s" class="%(css)s">',
            {
                "id": divid,
                "css": "releditField",
                "out": "jQuery('#%s').addClass('invisible')" % divid,
                "over": "jQuery('#%s').removeClass('invisible')" % divid,
            },
            escape=False,
        )
        self.w('<div id="%s-value" class="editableFieldValue">', divid)
        self.w(value)
        self.w("</div>")
        form.render(w=self.w, renderer=renderer)
        self.w('<div id="%s" class="editableField invisible">', divid)

    def _edit_action(self, divid, args, edit_related, add_related, _delete_related):
        # XXX disambiguate wrt edit_related
        if not add_related:  # currently, excludes edition
            args["formid"] = "edition" if edit_related else "base"
            args["action"] = "edit_related" if edit_related else "edit_rtype"
            self.w(
                '<div id="%s-update" class="editableField" onclick="%s" title="%s">',
                divid,
                self._onclick % args,
                self._cw._(self._editzonemsg),
            )
            self.w(self._build_edit_zone())
            self.w("</div>")

    def _add_action(self, divid, args, _edit_related, add_related, _delete_related):
        if add_related:
            args["formid"] = "edition"
            args["action"] = "add"
            self.w(
                '<div id="%s-add" class="editableField" onclick="%s" title="%s">',
                divid,
                self._onclick % args,
                self._cw._(self._addmsg),
            )
            self.w(self._build_add_zone())
            self.w("</div>")

    def _del_action(self, divid, args, _edit_related, _add_related, delete_related):
        if delete_related:
            args["formid"] = "deleteconf"
            args["action"] = "delete"
            self.w(
                '<div id="%s-delete" class="editableField" onclick="%s" title="%s">',
                divid,
                self._onclick % args,
                self._cw._(self._deletemsg),
            )
            self.w(self._build_delete_zone())
            self.w("</div>")

    def _close_form_wrapper(self):
        self.w("</div>")
        self.w("</div>")

    def view_form(
        self,
        divid,
        value,
        form=None,
        renderer=None,
        edit_related=False,
        add_related=False,
        delete_related=False,
    ):
        self._open_form_wrapper(
            divid, value, form, renderer, edit_related, add_related, delete_related
        )
        args = form.event_args.copy()
        self._edit_action(divid, args, edit_related, add_related, delete_related)
        self._add_action(divid, args, edit_related, add_related, delete_related)
        self._del_action(divid, args, edit_related, add_related, delete_related)
        self._close_form_wrapper()


@ajaxfunc(output_type="xhtml")
def reledit_form(self):
    req = self._cw
    args = dict(
        (x, req.form[x]) for x in ("formid", "rtype", "role", "reload", "action")
    )
    rset = req.eid_rset(int(self._cw.form["eid"]))
    try:
        args["reload"] = json.loads(args["reload"])
    except ValueError:  # not true/false, an absolute url
        assert args["reload"].startswith("http")
    view = req.vreg["views"].select("reledit", req, rset=rset, rtype=args["rtype"])
    return self._call_view(view, **args)
