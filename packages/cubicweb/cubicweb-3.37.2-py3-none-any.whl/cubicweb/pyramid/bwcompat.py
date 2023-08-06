# copyright 2017 LOGILAB S.A. (Paris, FRANCE), all rights reserved.
# copyright 2014-2016 UNLISH S.A.S. (Montpellier, FRANCE), all rights reserved.
#
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

"""Backward compatibility layer for CubicWeb to run as a Pyramid application."""

import inspect
import logging
import sys
import traceback
from datetime import datetime

import pyramid
from pyramid import httpexceptions
from pyramid import security
from pyramid import tweens
from pyramid.csrf import check_csrf_token, check_csrf_origin, get_csrf_token
from pyramid.httpexceptions import HTTPSeeOther, HTTPException
from pyramid.settings import asbool

import cubicweb
import cubicweb.web
from cubicweb.debug import emit_to_debug_channel
from cubicweb.pyramid.core import cw_to_pyramid
from cubicweb.pyramid.csrf import CWCookieCSRFStoragePolicy
from cubicweb.web import LogOut, PublishException
from cubicweb.web.application import CubicWebPublisher

log = logging.getLogger(__name__)


class PyramidSessionHandler(object):
    """A CW Session handler that rely on the pyramid API to fetch the needed
    informations.

    It implements the :class:`cubicweb.web.application.CookieSessionHandler`
    API.
    """

    def __init__(self, appli):
        self.appli = appli

    def get_session(self, req):
        return req._request.cw_session

    def logout(self, req, goto_url):
        raise LogOut(url=goto_url)


class CubicWebPyramidHandler(object):
    """A Pyramid request handler that rely on a cubicweb instance to do the
    whole job

    :param appli: A CubicWeb 'Application' object.
    """

    def __init__(self, appli, cubicweb_config):
        self.appli = appli

        if cubicweb_config["query-log-file"]:
            self._query_log = open(cubicweb_config["query-log-file"], "a")
            self._write_to_log = self._write_to_log_file
        else:
            self._write_to_log = self._write_to_logger

    def _write_to_log_file(self, text):
        self._query_log.write(text)
        self._query_log.flush()

    def _write_to_logger(self, text):
        log.info(text)

    def __call__(self, request):
        """
        Handler that mimics what CubicWebPublisher.main_handle_request and
        CubicWebPublisher.core_handle do
        """

        cubicweb_request = request.cw_request
        cubicweb_registry = request.registry["cubicweb.registry"]

        try:
            content = None
            try:
                with cw_to_pyramid(request):
                    controller_id, rset = self.appli.url_resolver.process(
                        cubicweb_request, cubicweb_request.path
                    )

                    try:
                        controller = cubicweb_registry["controllers"].select(
                            controller_id, cubicweb_request, appli=self.appli
                        )
                    except cubicweb.NoSelectableObject as ex:
                        warning_message = (
                            "failed to select a controller for this request "
                            f"{cubicweb_request.path} {request.method}."
                        )

                        if ex.objects:
                            candidates = "\n * ".join(repr(x) for x in ex.objects)
                            warning_message += (
                                " Here were the candidates controllers (but none matched): \n * "
                                f"{candidates}"
                            )
                        else:
                            warning_message += " There was no candidate controller."

                        log.warning(warning_message)

                        raise httpexceptions.HTTPBadRequest(
                            cubicweb_request._(
                                "couldn't handle this request as it is either badly formed or is "
                                "lacking the correct authorizations"
                            )
                        )

                    get_csrf_token(
                        request
                    )  # ensure that we have a CSRF token on all requests
                    safe_methods = frozenset(["GET", "HEAD", "OPTIONS", "TRACE"])
                    if request.method not in safe_methods and getattr(
                        controller, "require_csrf", True
                    ):
                        check_csrf_token(request)
                        check_csrf_origin(request)

                    self._write_to_log(
                        "REQUEST [%s] '%s' selected controller %s at %s:%s"
                        % (
                            controller_id,
                            cubicweb_request.path,
                            controller,
                            inspect.getsourcefile(controller.__class__),
                            inspect.getsourcelines(controller.__class__)[1],
                        )
                    )
                    emit_to_debug_channel(
                        "vreg",
                        {
                            "vreg": cubicweb_registry,
                        },
                    )
                    emit_to_debug_channel(
                        "controller",
                        {
                            "kind": controller_id,
                            "request": cubicweb_request,
                            "path": cubicweb_request.path,
                            "controller": controller,
                            "config": self.appli.repo.config,
                        },
                    )

                    cubicweb_request.update_search_state()
                    content = controller.publish(rset=rset)

                    # XXX this auto-commit should be handled by the cw_request
                    # cleanup or the pyramid transaction manager.
                    # It is kept here to have the ValidationError handling bw
                    # compatible
                    if cubicweb_request.cnx:
                        transaction_uuid = cubicweb_request.cnx.commit()
                        # commited = True
                        if transaction_uuid is not None:
                            cubicweb_request.data[
                                "last_undoable_transaction"
                            ] = transaction_uuid
            except cubicweb.web.ValidationError as ex:
                # XXX The validation_error_handler implementation is light, we
                # should redo it better in cw_to_pyramid, so it can be properly
                # handled when raised from a cubicweb view.
                # BUT the real handling of validation errors should be done
                # earlier in the controllers, not here. In the end, the
                # ValidationError should never by handled here.
                content = self.appli.validation_error_handler(cubicweb_request, ex)
            except cubicweb.web.RemoteCallFailed as exception:
                raise pyramid.httpexceptions.exception_response(
                    exception.status,
                    body=exception.dumps(),
                    content_type="application/json",
                    charset="utf-8",
                )

            if content is not None:
                request.response.body = content

        except LogOut as ex:
            # The actual 'logging out' logic should be in separated function
            # that is accessible by the pyramid views
            headers = security.forget(request)
            raise HTTPSeeOther(ex.url, headers=headers)
        except cubicweb.AuthenticationError:
            # Will occur upon access to cubicweb_request.cnx which is a
            # cubicweb.dbapi._NeedAuthAccessMock.
            if not content:
                raise HTTPSeeOther("/login")
        except cubicweb.web.NotFound as ex:
            view = cubicweb_registry["views"].select("404", cubicweb_request)
            content = cubicweb_registry["views"].main_template(
                cubicweb_request, view=view
            )
            request.response.status_code = ex.status
            request.response.body = content
        finally:
            # XXX CubicWebPyramidRequest.headers_out should
            # access directly the pyramid response headers.
            request.response.headers.clear()
            for (
                header_name,
                header_values,
            ) in cubicweb_request.headers_out.getAllRawHeaders():
                for item in header_values:
                    request.response.headers.add(header_name, item)

        return request.response

    def error_handler(self, exc, request):
        req = request.cw_request
        if isinstance(exc, httpexceptions.HTTPException):
            request.response = exc
        elif isinstance(exc, PublishException) and exc.status is not None:
            request.response = httpexceptions.exception_response(exc.status)
        else:
            request.response = httpexceptions.HTTPInternalServerError()
        request.response.cache_control = "no-cache"
        vreg = request.registry["cubicweb.registry"]
        excinfo = sys.exc_info()
        req.reset_message()
        if req.ajax_request:
            content = self.appli.ajax_error_handler(req, exc)
        else:
            try:
                req.data["ex"] = exc
                req.data["excinfo"] = excinfo
                errview = vreg["views"].select("error", req)
                template = self.appli.main_template_id(req)
                content = vreg["views"].main_template(req, template, view=errview)
            except Exception:
                content = vreg["views"].main_template(req, "error-template")
        log.exception(exc)
        request.response.body = content
        return request.response


class TweenHandler(object):
    """A Pyramid tween handler that submit unhandled requests to a Cubicweb
    handler.

    The CubicWeb handler to use is expected to be in the pyramid registry, at
    key ``'cubicweb.handler'``.
    """

    def __init__(self, handler, registry):
        self.handler = handler
        self.cwhandler = registry["cubicweb.handler"]

    def __call__(self, request):
        view_kind = "pyramid"
        now = str(datetime.now()).split(".")[0]

        try:
            try:
                response = self.handler(request)
            except httpexceptions.HTTPNotFound:
                view_kind = "cubicweb"
                response = self.cwhandler(request)

            print(
                f"{now} - ({view_kind} view) "
                f'"{request.method} {request.path}'
                f' {request.http_version}" '
                f"{response.status_code} {len(response.body)}"
            )

        except HTTPException as e:
            print(
                f'{now} - ({view_kind} view) "{request.method} '
                f'{request.path} {request.http_version}" '
                f"{e.code} {len(e.body)}"
            )

            # we don't want a traceback for a redirection, only for errors or others
            if not (300 <= e.code < 400):
                traceback.print_exc()
            raise

        return response


def includeme(config):
    """Set up a tween app that will handle the request if the main application
    raises a HTTPNotFound exception.

    This is to keep legacy compatibility for cubes that makes use of the
    cubicweb urlresolvers.

    It provides, for now, support for cubicweb controllers, but this feature
    will be reimplemented separatly in a less compatible way.

    It is automatically included by the configuration system, but can be
    disabled in the :ref:`pyramid_settings`:

    .. code-block:: ini

        cubicweb.bwcompat = no
    """
    cwconfig = config.registry["cubicweb.config"]
    repository = config.registry["cubicweb.repository"]
    cwappli = CubicWebPublisher(
        repository, cwconfig, session_handler_fact=PyramidSessionHandler
    )
    cwhandler = CubicWebPyramidHandler(cwappli, cwconfig)

    config.registry["cubicweb.appli"] = cwappli
    config.registry["cubicweb.handler"] = cwhandler

    config.add_tween("cubicweb.pyramid.bwcompat.TweenHandler", under=tweens.EXCVIEW)

    config.set_default_csrf_options(require_csrf=True)
    config.set_csrf_storage_policy(CWCookieCSRFStoragePolicy())

    if asbool(config.registry.settings.get("cubicweb.bwcompat.errorhandler", True)):
        config.add_view(cwhandler.error_handler, context=Exception)
        # XXX why do i need this?
        config.add_view(cwhandler.error_handler, context=httpexceptions.HTTPForbidden)
