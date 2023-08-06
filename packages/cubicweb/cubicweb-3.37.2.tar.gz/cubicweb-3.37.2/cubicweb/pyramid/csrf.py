import logging

from pyramid.csrf import CookieCSRFStoragePolicy

logger = logging.getLogger("cubicweb.pyramid.security.csrf")


class CWCookieCSRFStoragePolicy(CookieCSRFStoragePolicy):
    """
    This class is exactly like CookieCSRFStoragePolicy except it includes debugging logging.
    """

    def check_csrf_token(self, request, supplied_token):
        """Returns ``True`` if the ``supplied_token`` is valid."""
        token_is_valid = super().check_csrf_token(request, supplied_token)
        if token_is_valid:
            logger.info(
                f"CSRF token is valid on request {request.method} {request.path}"
            )
        else:
            if supplied_token:
                logger.warning(
                    f"CSRF token is different from the expected token on request {request.method} {request.path}"
                )
            elif request.method == "POST":
                logger.warning(
                    f"no CSRF token has been supplied on {request.method} {request.path}, you need to pass it in the form parameter or as the X-CSRF-Token header"
                )
            else:
                logger.warning(
                    f"no CSRF token has been supplied on {request.method} {request.path}, you need to pass it as the X-CSRF-Token header"
                )

        return token_is_valid

    def new_csrf_token(self, request):
        logger.debug("generate a new CSRF token")
        return super().new_csrf_token(request)
