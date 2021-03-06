repoze.urchin Changelog
=======================

Unreleased
----------

-

0.2 (2011-10-10)
----------------

- Replaced urchin javascript with new async tracking code. See:

    http://www.google.com/support/googleanalytics/bin/answer.py?answer=174090

  Note that the script is now inserted at the end of the <head> tag.

- Added bypass for HEAD requests. This is a workaround for an assertion in
  webob.Response that doesn't let you set the body on a response if the request
  method is 'HEAD'. This behavior on the part of webob is actually bogus, as
  outlined here:

    http://blog.dscpl.com.au/2009/10/wsgi-issues-with-http-head-requests.html

  The key issue here is that as long as anything in the WSGI stack tries to
  special case 'HEAD' requests, we can end up with responses with headers which
  differ depending on whether the request method is 'GET' or 'HEAD'.  In this
  specific example, by bypassing the urchin processing in the event of a HEAD
  request, we wind up with a Content-Length header for HEAD that doesn't
  include the extra bytes for the inserted urchin code that we would get with a
  GET request. This is, by definition of the standards, wrong, and yet
  unavoidable as long as webob is in our stack.

  For now, we can hold our noses and know that probably nothing's going to
  really break because of this discrepency, but we can maybe try to convince
  the webob crowd to drop conditional processing for HEAD requests.

0.1 (2009-06-02)
----------------

- Initial release.
