from webob import Request

URCHIN_TAGS = """
<script src="https://ssl.google-analytics.com/urchin.js"
        type="text/javascript">
</script>
<script type="text/javascript">
_uacct = "%s"; urchinTracker();
</script>
"""

class UrchinMiddleware(object):

    def __init__(self, app, account):
        self.app = app
        self.account = account

    def __call__(self, environ, start_response):
        req = Request(environ)
        resp = req.get_response(self.app)
        if resp.content_type == 'text/html':
            body = resp.body
            before = '</body>'
            after = (URCHIN_TAGS % self.account) + '</body>'
            resp.body = body.replace(before, after, 1)
        return resp(environ, start_response)


def make_middleware(app, global_conf=None, **kw):
    return UrchinMiddleware(app, kw['account'])
