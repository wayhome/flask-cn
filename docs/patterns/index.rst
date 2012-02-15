.. _patterns:

Flask的模式
==================
:译者: fermin.yang#gmail.com

在众多Web应用里，很多情况下你都能找到一些共同点。举个例子，许多应用都使用了关系型数据库和用户认证。在这种情况下就需要在请求开始时打开数据库连接并且获取当前登录用户的相关信息。在请求结束时，就需要再次关闭数据库连接。

在 `Flask 语块库 <http://flask.pocoo.org/snippets/>`_ 里，你能找到更多类似的模块或模式的应用。 

.. toctree::
   :maxdepth: 2

   packages
   appfactories
   appdispatch
   urlprocessors
   distribute
   fabric
   sqlite3
   sqlalchemy
   fileuploads
   caching
   viewdecorators
   wtforms
   templateinheritance
   flashing
   jquery
   errorpages
   lazyloading
   mongokit
   favicon
