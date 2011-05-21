.. _tutorial-introduction:

介绍 Flaskr
===========

这里我们把我们的blog程序叫做flaskr，你可以选一个不那么web 2.0的名字 ;) 
基本上我们想让它晚餐如下的功能 :

1. 根据配置文件里面的认证信息让用户登陆登出。只支持一个用户
2. 用户登陆后，可以向页面添加文章，题目只能是纯文字，内容可以使用一部分
   的HTML语言。这里我们假设用户是可信任的，所以对输入的HTML不会进行处理
3. 页面以倒序的顺序（后发布的在上方），在一个页面中显示所有的文章。用户
   登陆后可以添加新文章。

我们为我们的应用选择SQLite3因为它对这种大小的应用足够了。但是更大的应用
就很有必要使用 `SQLAlchemy`_ ，它更加智能的处理数据库连接，通过它可以一
次连接到不同的关系数据库而且可以做到更多。你也可以考虑使用最流行NoSQL数
据库之一如果你的数据更加适合这类数据库。

这是来自最终应用的一个截图:

.. image:: ../_static/flaskr.png
    :align: center
    :class: screenshot
    :alt: screenshot of the final application

继续 :ref:`tutorial-folders`.

.. _SQLAlchemy: http://www.sqlalchemy.org/
