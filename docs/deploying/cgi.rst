CGI
===

即使所有其他的部署方法都不行，CGI一定行！
所有主流的服务器都支持CGI，只不过这个不是首选的解决方案。 

这也是一种将你的Flask应用架设在Google的 `App Engine`_ 上的一种方法，或者其他任何和CGI类似的环境下。

.. admonition:: 注意

   请事先确认你应用程序内的所有 ``app.run()`` 调用包含在 ``if __name__ ==  '__main__':`` 区块内或在一个单独的文件里。 要确认这个的原因是因为这句语句执行后总是会启动一个新的本地WSGI服务器，但在部署到CGI / app的环境中，我们不需要它。 

创建一个 `.cgi` 文件
----------------------

首先你要创建一个CGI应用文件。我们先给它起个名字，就叫它 `yourapplication.cgi`::

    #!/usr/bin/python
    from wsgiref.handlers import CGIHandler
    from yourapplication import app

    CGIHandler().run(app)

服务器设置
------------

配置服务器通常有两种方法。直接将 `.cgi` 文件拷贝到一个 `cgi-bin` （并且使用 `mod_rewrite` 或者其他类似的东西来重写URL）或者将服务器直接指向文件。

例如在Apache环境下，你可以在配置文件内加入以下内容:

.. sourcecode:: apache

    ScriptAlias /app /path/to/the/application.cgi

如你需要更多的信息请参考你使用的web服务器的文档。

.. _App Engine: http://code.google.com/appengine/
