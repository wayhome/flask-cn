.. _deploying-other-servers:

其他服务器
=============

现在还有许多十分流行的由Python编写的服务器可以执行WSGI应用。这些服务器在执行时会独立运行；你可以在你的web服务器上设置反向代理来使用它们。

Tornado
--------

`Tornado`_ 是一个可扩展的，non-blocking（非阻塞）的开源服务器和工具，且提供了 `FriendFeed`_ 。因为它是non-blocking的且使用了epoll，它可以同时处理几千个连接，这意味着它是一个理想的实时web服务器。将它与Flask集成更是小菜一碟::

    from tornado.wsgi import WSGIContainer
    from tornado.httpserver import HTTPServer
    from tornado.ioloop import IOLoop
    from yourapplication import app

    http_server = HTTPServer(WSGIContainer(app))
    http_server.listen(5000)
    IOLoop.instance().start()


.. _Tornado: http://www.tornadoweb.org/
.. _FriendFeed: http://friendfeed.com/

Gevent
-------

`Gevent`_ 是一个基于协程的Python网络类库，它使用了 `greenlet`_ 来提供在 `libevent`_ 事件循环顶端的高级别异步API::

    from gevent.wsgi import WSGIServer
    from yourapplication import app

    http_server = WSGIServer(('', 5000), app)
    http_server.serve_forever()

.. _Gevent: http://www.gevent.org/
.. _greenlet: http://codespeak.net/py/0.9.2/greenlet.html
.. _libevent: http://monkey.org/~provos/libevent/

Gunicorn
--------

`Gunicorn`_ 'Green Unicorn' 是一个UNIX下的WSGI HTTP服务器。它是一个早期从Ruby的Unicorn项目分流出来的项目。它同时支持 `eventlet`_ 和 `greenlet`_ 。在该服务器上运行Flask应用也是非常简单的::

    gunicorn myproject:app

`Gunicorn`_ 提供了许多命令行的操作方式 -- 请查看 ``gunicorn -h`` 。举个例子，使用4个工作进程来执行Flask应用 (``-w4``) 绑定在localhost的4000端口上 (``-b 127.0.0.1:4000``)::

    gunicorn -w 4 -b 127.0.0.1:4000 myproject:app

.. _Gunicorn: http://gunicorn.org/
.. _eventlet: http://eventlet.net/
.. _greenlet: http://codespeak.net/py/0.9.2/greenlet.html

反向代理设置
------------

如果你将你的应用部署在上述其中一个服务器上且放置在某个已设置反向代理的HTTP服务器后面，你需要重写一些头来让你的应用正常工作。通常在WSGI环境下会导致问题产生的值是 `REMOTE_ADDR` 和 `HTTP_HOST` 。Werkzeug已经搭载了一些常见设置的解决方法，但是你可能希望为某些特殊的情况自己写WSGI中间件。

这种情况下一般要设定的值是 `X-Forwarded-Host` 转发到哪里和 `X-Forwarded-For` 从哪里转发的::

    from werkzeug.contrib.fixers import ProxyFix
    app.wsgi_app = ProxyFix(app.wsgi_app)

请记住在无反向代理的设置下使用这样一个中间件会造成一定的安全隐患，因为会信任那些可能由恶意用户伪造传入的头。

如果你需要重写头，你可能需要使用如下方法::

    class CustomProxyFix(object):

        def __init__(self, app):
            self.app = app

        def __call__(self, environ, start_response):
            host = environ.get('HTTP_X_FHOST', '')
            if host:
                environ['HTTP_HOST'] = host
            return self.app(environ, start_response)

    app.wsgi_app = CustomProxyFix(app.wsgi_app)
