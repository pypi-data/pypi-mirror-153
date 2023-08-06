.. _csrf_protection:

CSRF protection in CubicWeb
===========================

*added in 3.31*

Introduction
------------

To quote `OWASP <https://owasp.org/www-community/attacks/csrf>`_, a CSRF is:

::

    Cross-Site Request Forgery (CSRF) is an attack that forces an end user to
    execute unwanted actions on a web application in which they’re currently
    authenticated. With a little help of social engineering (such as sending a
    link via email or chat), an attacker may trick the users of a web
    application into executing actions of the attacker’s choosing. If the
    victim is a normal user, a successful CSRF attack can force the user to
    perform state changing requests like transferring funds, changing their
    email address, and so forth. If the victim is an administrative account,
    CSRF can compromise the entire web application.

This is especially dangerous for every website where the users are able to do
modification requests (for exemple by submitting a form).

The way the protection is done is:

- the user asks a page with a form
- the website generates a unique token for this user
- the token is then inserted in the form as a hidden field
- the user gets the page with the form
- when the user clics on the "submit" button of the form, the token is sent to the server
- there, the server checks that the token is the same as the one generated
- this ensures that this is the user that has made the request and has not been
  tricked in doing it without its knowledge

In an AJAX/frontend context, the behavior is a bit different and is handled by
how the frontend has built its strategy.

Implementation in CubicWeb
--------------------------

CubicWeb offers a CSRF protection by default by integrating `Pyramid's CSRF
middleware
<https://docs.pylonsproject.org/projects/pyramid/en/latest/narr/security.html#preventing-cross-site-request-forgery-attacks>`_.

The CSRF Policy used by CubicWeb is `CookieCSRFStoragePolicy
<https://docs.pylonsproject.org/projects/pyramid/en/latest/api/csrf.html#pyramid.csrf.CookieCSRFStoragePolicy>`_
which inserts the CSRF token in:

- every CubicWeb forms by default (except if you have been doing weird things
  in the way forms are rendered),
- in the cookie at the "csrf_token" key, which can be useful if you are doing
  ajax requests without first getting a form.

Adding the CSRF token in a CubicWeb Form
----------------------------------------

By default you don't have to do anything as it is added in all forms, but if
for any reason you need to do it, it's done like this in CubicWeb:

.. code:: python

    from pyramid.csrf import get_csrf_token


    # in the form generation part which here is Form.__init__
    # here req is a CubicWeb request in the context of CubicWeb using pyramid
    # here req._request is the pyramid request
    token = get_csrf_token(req._request)
    self.add_hidden("csrf_token", token)

Using the CSRF token in a pyramid context
-----------------------------------------

Your main source of information is the `Pyramid documentation
<https://docs.pylonsproject.org/projects/pyramid/en/latest/narr/security.html#using-the-csrf-get-csrf-token-method>`_.
on csrf. It explains how to `get the token
<https://docs.pylonsproject.org/projects/pyramid/en/latest/narr/security.html#using-the-csrf-get-csrf-token-method>`_,
verify the token and `integrate the token in a jinja2 template
<https://docs.pylonsproject.org/projects/pyramid/en/latest/narr/security.html#using-the-get-csrf-token-global-in-templates>`_
and also `disabling the CSRF protection if needed
<https://docs.pylonsproject.org/projects/pyramid/en/latest/narr/security.html#checking-csrf-tokens-automatically>`_.

Using the CSRF token in a pyramid context depends on how views are built. To
get the token, one can use `get_csrf_token(request)
<https://docs.pylonsproject.org/projects/pyramid/en/latest/api/csrf.html#pyramid.csrf.LegacySessionCSRFStoragePolicy.get_csrf_token>`_
method from `pyramid.csrf`.

Grabbing the CSRF token from the cookie using javascript
--------------------------------------------------------

The logic is exactly the same as in `Django js snippet
<https://docs.djangoproject.com/en/3.2/ref/csrf/#acquiring-the-token-if-csrf-use-sessions-and-csrf-cookie-httponly-are-false>`_
except the key for the cookie that is different.

Therefore you'll need this code or an adapted version for your frontend code:

.. code:: javascript

    function getCookie(name) {
        let cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            const cookies = document.cookie.split(';');
            for (let i = 0; i < cookies.length; i++) {
                const cookie = cookies[i].trim();
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    const token = getCookie('csrf_token');

To quote and adapt Django's documentation: the above code could be simplified
by using the `JavaScript Cookie library
<https://github.com/js-cookie/js-cookie/>`_ to replace getCookie:

.. code:: javascript

    const csrftoken = Cookies.get('csrf_token');

Submitting the CSRF token using AJAX
------------------------------------

Once you have grab the CSRF token like describe in the previous section, you
need to submit it as **HTTP Header** `X-CSRF-Token`.

To quote Pyramid documentation, if you are using jQuery here is how you can do it:

.. code:: javascript

    var csrfToken = "${get_csrf_token()}";

    $.ajax({
      type: "POST",
      url: "/myview",
      headers: { 'X-CSRF-Token': csrfToken }
    }).done(function() {
      alert("Deleted");
    });

Submitting the CSRF token for a request with the content/type "application/json"
--------------------------------------------------------------------------------

Exactly like an AJAX request, once you have the CSRF token as
explained in the previous section, you need to submit it as **HTTP
Header** `X-CSRF-Token`

Manually checking the CSRF token
--------------------------------

If for wathever reason you need to manually check the CSRF token, here is how
it's done in CubicWeb (in
`cubicweb.pyramid.bwcompat.CubicWebPyramidHandler.__call__`):

.. code:: python

    from pyramid.csrf import check_csrf_token, check_csrf_origin

    safe_methods = frozenset(["GET", "HEAD", "OPTIONS", "TRACE"])
    if request.method not in safe_methods and getattr(
        controller, "require_csrf", True
    ):
        check_csrf_token(request)
        check_csrf_origin(request)

Here `check_csrf_origin` is a complementary CSRF protection.

Disable CSRF for a CubicWeb View
--------------------------------

By default, all CubicWeb views need a validation by CSRF token for every HTTP
request which are not GET, HEAD, OPTIONS or TRACE. To disable this comportment
in one view, you have to define a new Controller with a `require_csrf`
attribute at `False`. Every route using this controller will be able to be
called without CSRF tokens. Of course, you can be more precise by adding more
rules in your controller, for instance adding condition on specific view
registry id, or connected user.

Here is an example on how to register a controller that disable csrf for all views:

.. code:: python

    from cubicweb.web.views.basecontrollers import ViewController


    class ControllerWithCSRFCheckDisabled(ViewController):
        require_csrf = False

    def registration_callback(vreg):
        self.vreg.register_and_replace(ControllerWithCSRFCheckDisabled, ViewController)


For a more specific behavior you'll need to overwrite the `publish` method and
decide which view needs a csrf protection.
