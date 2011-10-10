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
                                body='<html><head></head></html>')
        mw = self._makeOne(app, account='123')
        environ = self._makeEnviron()
        app_iter = mw(environ, self._startResponse)

        body = list(app_iter)[0]
        self.assertEqual(body, """\
<html><head>
<script type="text/javascript">

  var _gaq = _gaq || [];
  _gaq.push(['_setAccount', '123']);
  _gaq.push(['_trackPageview']);

  (function() {
    var ga = document.createElement('script'); ga.type = 'text/javascript'; ga.async = true;
    ga.src = ('https:' == document.location.protocol ? 'https://ssl' : 'http://www') + '.google-analytics.com/ga.js';
    var s = document.getElementsByTagName('script')[0]; s.parentNode.insertBefore(ga, s);
  })();

</script>
</head></html>""")
        self.assertEqual(self._started[0], '200 OK')
        self.failUnless(('Content-Type', 'text/html') in self._started[1])

    def test_response_HEAD_request(self):
        app = DummyApp(headers=[('Content-Type', 'text/html')],
                                body='<html><head></head></html>')
        mw = self._makeOne(app)
        environ = self._makeEnviron(REQUEST_METHOD='HEAD')
        app_iter = mw(environ, self._startResponse)
        self.assertEqual(list(app_iter), ['<html><head></head></html>'])
        self.assertEqual(self._started[0], '200 OK')
        self.assertEqual(self._started[1], [('Content-Type', 'text/html')])

class DummyApp:

    def __init__(self, status='200 OK', headers=(), body=''):
        self.status = status
        self.headers = list(headers)
        self.body_chunks = [body]

    def __call__(self, environ, start_response):
        start_response(self.status, self.headers)
        return self.body_chunks
