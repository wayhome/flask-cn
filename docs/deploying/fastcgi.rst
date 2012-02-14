.. _deploying-fastcgi:

FastCGI
=======

FastCGI是一架设在诸如 `nginx`_, `lighttpd`_, 还有  `cherokee`_ 等服务器上的部署方式，请查阅 :ref:`deploying-uwsgi` 和 :ref:`deploying-other-servers` 获取关于上述方式的详细内容。在将你的WSGI应用架设到上述服务器上之前，你还需要一个FastCGI服务器。目前最流行的是 `flup`_ ，我们将在本向导里使用它。请确认将其安装在环境内。

.. admonition:: 注意

   请事先确认你应用程序内的所有 ``app.run()`` 调用包含在 ``if __name__ ==  '__main__':`` 区块内或在一个单独的文件里。 要确认这个的原因是因为这句语句执行后总是会启动一个新的本地WSGI服务器，但在部署到FastCGI的环境中，我们不需要它。 

创建一个 `.fcgi` 文件
-----------------------

首先你需要创建一个FastCGI服务器文件。我们给它起了名字，就叫它 `yourapplication.fcgi`::

    #!/usr/bin/python
    from flup.server.fcgi import WSGIServer
    from yourapplication import app

    if __name__ == '__main__':
        WSGIServer(app).run()

这已经足够让Apache正常工作了，不过nginx和老版本的lighttpd需要一个socket（套接字）来使与FastCGI服务器之间的通信更加明确。为了实现这一点你需要将socket的路径传到 :class:`~flup.server.fcgi.WSGIServer` 类里::

    WSGIServer(application, bindAddress='/path/to/fcgi.sock').run()

这里的路径必须与你在服务器配置文件内定义的完全一致。

将 `yourapplication.fcgi` 文件保存在你能找得到的地方。
比如在 `/var/www/yourapplication` 或类似的地方就比较靠谱。

确认这个文件上有服务器可以的执行权限:

.. sourcecode:: text

    # chmod +x /var/www/yourapplication/yourapplication.fcgi

配置 lighttpd
--------------------

lighttpd的FastCGI基本配置如下::

    fastcgi.server = ("/yourapplication.fcgi" =>
        ((
            "socket" => "/tmp/yourapplication-fcgi.sock",
            "bin-path" => "/var/www/yourapplication/yourapplication.fcgi",
            "check-local" => "disable",
            "max-procs" -> 1
        ))
    )

    alias.url = (
        "/static/" => "/path/to/your/static"
    )

    url.rewrite-once = (
        "^(/static.*)$" => "$1",
        "^(/.*)$" => "/yourapplication.fcgi$1"

记住要启用FastCGI, alias和rewrite模块。上述配置将要发布的应用绑定到了 `/yourapplication` 路径下。如果你希望将应用配置在根目录执行，那你就不得不先研究 :class:`~werkzeug.contrib.fixers.LighttpdCGIRootFix` 这个中间件来搞定lighttpd中的bug。

确认仅在你确实需要将你的应用配置到根目录时应用这个中间件。另外，如果需要了解更多信息也可以去看Lighty关于 `FastCGI and
Python <http://redmine.lighttpd.net/wiki/lighttpd/Docs:ModFastCGI>`_ 的文档（注意Lighty文档里提到的将socket传给run()的部分已经不需要了）。


配置 nginx
-----------------

在nginx上安装FastCGI稍微有些不同，因为在默认情况下nginx没有提供FastCGI参数。

基本的在nginx下的flask FastCGI配置如下::

    location = /yourapplication { rewrite ^ /yourapplication/ last; }
    location /yourapplication { try_files $uri @yourapplication; }
    location @yourapplication {
        include fastcgi_params;
	fastcgi_split_path_info ^(/yourapplication)(.*)$;
        fastcgi_param PATH_INFO $fastcgi_path_info;
        fastcgi_param SCRIPT_NAME $fastcgi_script_name;
        fastcgi_pass unix:/tmp/yourapplication-fcgi.sock;
    }

上述配置将要发布的应用绑定到了 `/yourapplication` 路径下。如果你希望将应用配置在根目录执行，这非常方便，因为你不需要考虑怎么算出 `PATH_INFO` 和 `SCRIPT_NAME` 的问题::

    location / { try_files $uri @yourapplication; }
    location @yourapplication {
        include fastcgi_params;
        fastcgi_param PATH_INFO $fastcgi_script_name;
        fastcgi_param SCRIPT_NAME "";
        fastcgi_pass unix:/tmp/yourapplication-fcgi.sock;
    }

执行 FastCGI 进程
-------------------------

既然 Nginx 和其他服务器不自动加载FastCGI的应用，你只好自己来了。 `管理员可以控制FastCGI进程 <http://supervisord.org/configuration.html#fcgi-program-x-section-settings>`_ 你也可以研究其他FastCGI进程的管理方法或者写一个脚本在系统启动时来运行你的 `.fcgi` 文件，举个例子，使用一个 SysV ``init.d`` 脚本。如果你是需要临时应付一下，你可以在GNU下直接执行 ``.fcgi`` 脚本然后不要去关它就好了。如需更多信息请看 ``man screen`` ，注意这是一个全手动的，重启后就只能再来一次::

    $ screen
    $ /var/www/yourapplication/yourapplication.fcgi

调试
---------

FastCGI的部署方式在大多数web服务器下都很难调试。很多情况下服务器的日志只能告诉你诸如 "premature end of headers" （网页个屁）的信息。为了要找出问题所在，你唯一能研究尝试的地方就是换一个确定能用的用户然后再次手动执行你的应用。 

这个例子假设你的应用叫做 `application.fcgi` ，你的web服务器用户是 `www-data`::

    $ su www-data
    $ cd /var/www/yourapplication
    $ python application.fcgi
    Traceback (most recent call last):
      File "yourapplication.fcgi", line 4, in <module>
    ImportError: No module named yourapplication

在这个例子里这个错误大多是因为 "yourapplication" 应用不在python能找到的路径里。这个问题通常出在：

-   使用了相对路径，且和当前工作目录没有关系。
-   部分代码需要调用环境变量，但是没有在web服务器内配置。
-   使用了其他python的解释器。

.. _nginx: http://nginx.org/
.. _lighttpd: http://www.lighttpd.net/
.. _cherokee: http://www.cherokee-project.com/
.. _flup: http://trac.saddi.com/flup
