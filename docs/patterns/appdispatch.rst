.. _app-dispatch:

应用程序的派遣
=======================

应用程序的派遣就是在WSGI层面上整合多个Flask应用程序的过程。你可以只将一些Flask应用整合到一个更大的WSGI应用里。甚至你需要的话也可以让Django和Flask应用由同一个解释器来并肩执行。至于如何具体分派那就要取决于应用程序在内部是如何工作的了。

这里谈到的内容与 :ref:`module approach <larger-applications>` 里说述的基本不同点是，你要执行的相同或不同的Flask应用之间是完全相互独立的。他们在WSGI层面上进行调度，且根据不同的配置执行。


关于本章节
--------------------------

下面提到的所有使用到的技术和例子，只要是在 ``application`` 对象内的，都可以由任何的WSGI服务器执行，如果你要配置生产环境，请看 :ref:`deployment` 章节。如果是开发环境，Werkzeug已经提供了供开发者使用的内嵌的服务器 :func:`werkzeug.serving.run_simple`::

    from werkzeug.serving import run_simple
    run_simple('localhost', 5000, application, use_reloader=True)

请注意 :func:`run_simple <werkzeug.serving.run_simple>` 不是用来作为生产环境使用的。请使用 :ref:`完备的WSGI服务器 <deployment>`.


整合应用程序
----------------------

如果你有几个完全分离的应用，但是你想让他们在同一个Python解释进程下协同工作，你可以使用 :class:`werkzeug.wsgi.DispatcherMiddleware` 里的功能。实现它的原理是每一个Flask应用都是一个合法的WSGI应用，那么他们可以用添加前缀的方式由派遣的中间件来整合成一个更大的应用。

举个例子，你可能希望让你的主应用在 `/` 路径下执行，而你的后台在 `/backend` 路径下执行::

    from werkzeug.wsgi import DispatcherMiddleware
    from frontend_app import application as frontend
    from backend_app import application as backend

    application = DispatcherMiddleware(frontend, {
        '/backend':     backend
    })


由子域名进行分派
---------------------

有时候你可能希望同时使用一个应用的多种不同版本的实例。假设应用的创建是在方法里实现的，你可以调用这个方法来对它进行实例化，这样的话实现起来就非常方便。如果你要了解如何让你的应用程序支持在方法里进行应用程序实例化操作，请查阅 :ref:`app-factories` 章节。

根据子域名创建应用是非常常见的。比如说你可能会对你的Web服务器进行配置，使其将所有的请求分派给你的应用程序来执行，然后你的应用程序根据子域名信息创建特定用户的实例。当你将你的服务器配置为监听所有的子域名后，你就能非常简单的用一个WSGI应用来实现动态应用的创建了。

WSGI层是处理这个问题的最佳着手点。你可以编写你自己的WSGI应用程序来查看请求的来源，然后把它委派给你的Flask应用去执行。如果那个应用不存在，那就动态的创建一个并且记住它::

    from threading import Lock

    class SubdomainDispatcher(object):

        def __init__(self, domain, create_app):
            self.domain = domain
            self.create_app = create_app
            self.lock = Lock()
            self.instances = {}

        def get_application(self, host):
            host = host.split(':')[0]
            assert host.endswith(self.domain), 'Configuration error'
            subdomain = host[:-len(self.domain)].rstrip('.')
            with self.lock:
                app = self.instances.get(subdomain)
                if app is None:
                    app = self.create_app(subdomain)
                    self.instances[subdomain] = app
                return app

        def __call__(self, environ, start_response):
            app = self.get_application(environ['HTTP_HOST'])
            return app(environ, start_response)


你可以这样调用这个派遣::

    from myapplication import create_app, get_user_for_subdomain
    from werkzeug.exceptions import NotFound

    def make_app(subdomain):
        user = get_user_for_subdomain(subdomain)
        if user is None:
            # if there is no user for that subdomain we still have
            # to return a WSGI application that handles that request.
            # We can then just return the NotFound() exception as
            # application which will render a default 404 page.
            # You might also redirect the user to the main page then
            return NotFound()

        # otherwise create the application for the specific user
        return create_app(user)

    application = SubdomainDispatcher('example.com', make_app)


根据路径分派
----------------

根据URL地址进行分派也十分类似。相对于查找 `Host` 头来确定子域名，这里你只需要查看请求网址第一个斜杠后的内容就可以了::

    from threading import Lock
    from werkzeug.wsgi import pop_path_info, peek_path_info

    class PathDispatcher(object):

        def __init__(self, default_app, create_app):
            self.default_app = default_app
            self.create_app = create_app
            self.lock = Lock()
            self.instances = {}

        def get_application(self, prefix):
            with self.lock:
                app = self.instances.get(prefix)
                if app is None:
                    app = self.create_app(prefix)
                    if app is not None:
                        self.instances[prefix] = app
                return app

        def __call__(self, environ, start_response):
            app = self.get_application(peek_path_info(environ))
            if app is not None:
                pop_path_info(environ)
            else:
                app = self.default_app
            return app(environ, start_response)

这里与子域名分派的最大不同点是如果创建的方法返回 `None` ，这里就会退到一个另外的应用程序里::

    from myapplication import create_app, default_app, get_user_for_prefix

    def make_app(prefix):
        user = get_user_for_prefix(prefix)
        if user is not None:
            return create_app(user)

    application = PathDispatcher('example.com', default_app, make_app)
