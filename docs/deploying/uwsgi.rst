.. _deploying-uwsgi:

uWSGI
=====

uWSGI是一架设在诸如 `nginx`_, `lighttpd`_, 还有 `cherokee`_ 等服务器上的部署方式，请查阅 :ref:`deploying-fastcgi` 和 :ref:`deploying-other-servers` 获取关于上述方式的详细内容。在将你的WSGI应用架设到上述服务器上之前，你还需要一个uWSGI服务器。uWSGI是一个应用服务器，同时也是一个协议服务器；它能够搭载uWSGI, FastCGI, 和 HTTP协议。

目前最流行的uWSGI服务器是 `uwsgi`_ ，我们将在本向导里使用它。请确认将其安装在环境内。

.. admonition:: 注意

   请事先确认你应用程序内的所有 ``app.run()`` 调用包含在 ``if __name__ ==  '__main__':`` 区块内或在一个单独的文件里。 要确认这个的原因是因为这句语句执行后总是会启动一个新的本地WSGI服务器，但在部署到uWSGI的环境中，我们不需要它。 

用uwsgi执行你的应用
----------------------------

`uwsgi` 被设计于在python模块里找到WSGI调用时进行相关操作。

假设在myapp.py里已有一个flask的应用，只要执行如下的命令：

.. sourcecode:: text

    $ uwsgi -s /tmp/uwsgi.sock --module myapp --callable app

或者，你也可以这样：

.. sourcecode:: text

    $ uwsgi -s /tmp/uwsgi.sock myapp:app

配置 nginx
-----------------

基本的基于nginx的flask uWSGI配置如下::

    location = /yourapplication { rewrite ^ /yourapplication/; }
    location /yourapplication { try_files $uri @yourapplication; }
    location @yourapplication {
      include uwsgi_params;
      uwsgi_param SCRIPT_NAME /yourapplication;
      uwsgi_modifier1 30;
      uwsgi_pass unix:/tmp/uwsgi.sock;
    }

上述配置将要发布的应用绑定到了 `/yourapplication` 路径下。如果你希望将应用配置在根目录执行，这非常方便，因为你只要不要去指定 `SCRIPT_NAME` 和设置uwsgi modifier就可以了::

    location / { try_files $uri @yourapplication; }
    location @yourapplication {
        include uwsgi_params;
        uwsgi_pass unix:/tmp/uwsgi.sock;
    }

.. _nginx: http://nginx.org/
.. _lighttpd: http://www.lighttpd.net/
.. _cherokee: http://www.cherokee-project.com/
.. _uwsgi: http://projects.unbit.it/uwsgi/
