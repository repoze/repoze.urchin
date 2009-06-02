import unittest

class UrchinMiddlewareTests(unittest.TestCase):

    def _getTargetClass(self):
        from repoze.urchin import UrchinMiddleware
        return UrchinMiddleware

    def _makeOne(self, app=None, account='UA-1234567-8'):
        if app is None:
            app = DummyApp()
        return self._getTargetClass()(app, account)

    def _makeEnviron(self, **kw):
        environ = {'REQUEST_METHOD': 'GET'}
        environ.update(kw)
        return environ

    def _startResponse(self, status, headers):
        self._started = (status, headers)

    def test_response_not_HTML(self):
        app = DummyApp(headers=[('Content-Type', 'text/plain')], body='xxx')
        mw = self._makeOne(app)
        environ = self._makeEnviron()
        app_iter = mw(environ, self._startResponse)
        self.assertEqual(list(app_iter), ['xxx'])
        self.assertEqual(self._started[0], '200 OK')
        self.assertEqual(self._started[1], [('Content-Type', 'text/plain')])

    def test_response_w_HTML(self):
        app = DummyApp(headers=[('Content-Type', 'text/html')],
                                body='<html><body></body></html>')
        mw = self._makeOne(app, account='123')
        environ = self._makeEnviron()
        app_iter = mw(environ, self._startResponse)

        body = list(app_iter)[0]
        self.assertEqual(body, """\
<html><body>
<script src="https://ssl.google-analytics.com/urchin.js"
        type="text/javascript">
</script>
<script type="text/javascript">
_uacct = "123"; urchinTracker();
</script>
</body></html>""")
        self.assertEqual(self._started[0], '200 OK')
        self.failUnless(('Content-Type', 'text/html') in self._started[1])


class DummyApp:

    def __init__(self, status='200 OK', headers=(), body=''):
        self.status = status
        self.headers = list(headers)
        self.body_chunks = [body]

    def __call__(self, environ, start_response):
        start_response(self.status, self.headers)
        return self.body_chunks
