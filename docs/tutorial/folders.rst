.. _tutorial-folders:

初始准备: 创建目录
================

在我们开始之前，让我们先创建应用所需的目录 ::

    /flaskr
        /static
        /templates

`flask`
目录不是python的package，只是我们放文件的地方。我们将要把我们在以后步骤
中用到的数据库模式和主要的模块放在这个目录中。 `static` 目录可以被网络
上的用户通过 `HTTP` 访问。css和javascript文件就存放在这个目录下。
Flask在 `template` 下查找 `jinja2`_ 的模版文件。把所有的模版文件放在这个
目录下。

继续 :ref:`tutorial-schema`.

.. _Jinja2: http://jinja.pocoo.org/2/
