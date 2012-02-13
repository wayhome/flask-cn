.. _deployment:

部署途径
==================
:译者: fermin.yang#gmail.com

你有很多种途径可以运行Flask应用程序，你可以根据实际情况进行选择。你当然可以直接使用内嵌的服务器，但是使用正规的部署方式来呈现产品更加靠谱。（就是说别在发布的服务器上偷懒用内嵌的啦。）你有很多种的选择，这里都将一一列出。

如果你要用其他的WSGI服务器请自行查阅关于如何使用WSGI app的服务器文档。你只要记住你的 :class:`Flask` 应用程序对象事实上就是一个WSGI应用程序就可以了。

.. toctree::
   :maxdepth: 2

   mod_wsgi
   cgi
   fastcgi
   uwsgi
   others
