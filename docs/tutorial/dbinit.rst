.. _tutorial-dbinit:

第三步： 创建一个数据库
=======================

我们原来就说过，Flask是一个数据去驱动的应用，更准确的来说，是一个基于关系数
据库的应用。这样的系统需要一个模式来决定怎么去存储信息。所以在第一次开启服
务器前就把模式创建好很重要。

这个模式可以通过管道的方式把 `schema.sql` 输入到 `sqlite3` 命令中，如下所示
 ::

    sqlite3 /tmp/flaskr.db < schema.sql

这种方法的缺点是需要安装sqlite3命令，但是并不是每一个系统中都有安装。而且你
必须给出数据库的路径，否则就会出错。添加一个函数来对数据库进行初始化是一个
不错的想法。

如果你想这么做，首先要从contextlib package中import 
:func:`contextlib.closing` 函数。如果你想用Python 2.5，那么还需要开启
`with` 声明，（从 `_future_` 中的import内容要在所以import的最前面）::

    from __future__ import with_statement
    from contextlib import closing

下面我们创建一个叫 `init_db` 的函数来初始化数据库。在这里，我们可以使用前面
定义的 `connect_db` 函数。只需要把这个函数添加到 `connect_db` 函数的下面::

    def init_db():
        with closing(connect_db()) as db:
            with app.open_resource('schema.sql') as f:
                db.cursor().executescript(f.read())
            db.commit()

通过 :func: `~contextlib.closing` 辅助函数，我们可以在 `with` 模块中保持数
据库连接。applicationg对象的 :func:`~flask.Flask.open_resource` 方法支持也
支持这个功能，所以我们可以在 `with` 模块中直接使用它。这个函数用来从这个应
用的所在位置（ `flaskr` 目录）打开一个文件，然后允许你通过它来读取文件。我
们在这里使用这个函数是为了在数据库连接上执行一个脚本。

当你连接到数据库后，我们就得到了一个连接对象（这里我们把它叫做 `db` ），这
个对象会给我们提供一个指针。这个指针有一个方法可以来执行完整的数据库命令。
最后，我们还要来提交我们对数据库所做的改变。如果你不明确的来提交修改，
SQLite3和其他的事务数据库都不会自动提交这些修改。

现在我们可以打开一个Pythonshell，然后import函数，调用函数。这样就能创建一个
数据库了::

>>> from flaskr import init_db
>>> init_db()

.. admonition:: Troubleshooting

   如果你得到了一个表无法被找到的异常，检查下，你是否调用了 `init_db` ，而
   且你表的名字是正确的（单数 复数问题）。

继续 :ref:`tutorial-dbcon`
