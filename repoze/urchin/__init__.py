from webob import Request

URCHIN_TAGS = """
<script type="text/javascript">

  var _gaq = _gaq || [];
  _gaq.push(['_setAccount', '%s']);
  _gaq.push(['_trackPageview']);

  (function() {
    var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
    ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
    var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
  })();

</script>
"""

class UrchinMiddleware(object):

    def __init__(self, app, account):
        self.app = app
        self.account = account

    def __call__(self, environ, start_response):
        if environ.get('REQUEST_METHOD') == 'HEAD':
            #  Bypass this middleware if the request method is 'HEAD'. This is
            #  a workaround for an assertion in webob.Response that doesn't
            #  let you set the body on a response if the request method is
            #  'HEAD'. This behavior on the part of webob is actually bogus,
            #  as outlined here:
            #
            #  http://blog.dscpl.com.au/2009/10/wsgi-issues-with-http-head-requests.html
            #
            #  The key issue here is that as long as anything in the WSGI
            #  stack tries to special case 'HEAD' requests, we can end up with
            #  responses with headers which differ depending on whether the
            #  request method is 'GET' or 'HEAD'. In this specific example, by
            #  bypassing the urchin processing in the event of a HEAD request,
            #  we wind up with a Content-Length header for HEAD that doesn't
            #  include the extra bytes for the inserted urchin code that we
            #  would get with a GET request. This is, by definition of the
            #  standards, wrong, and yet unavoidable as long as webob is in
            #  our stack.
            #
            #  For now, we can hold our noses and know that probably nothing's
            #  going to really break because of this discrepency, but we can
            #  maybe try to convince the webob crowd to drop conditional
            #  processing for HEAD requests.
            #
            return self.app(environ, start_response)
        req = Request(environ)
        resp = req.get_response(self.app)
        if resp.content_type == 'text/html':
            body = resp.body
            before = '</head>'
            after = (URCHIN_TAGS % self.account) + '</head>'
            resp.body = body.replace(before, after, 1)
        return resp(environ, start_response)


def make_middleware(app, global_conf=None, **kw):
    return UrchinMiddleware(app, kw['account'])
