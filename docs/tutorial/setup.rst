.. _例程构建:

第二步: 应用程序构建代码
==============================

现在我们已经准备好了模式，终于可以创建应用程序的模块了。让我们把他叫做
`flaskr.py` ，并把它放在 `flaskr` 目录下。首先，我们把需要的模块和配置
导入。如果是小应用的话，可以直接把配置放在主模块里面，就跟我们将要做的
一样。但是一个更加清晰的方案是创建一个独立的 `.ini` 或 `.py` 文件，然
后导入或装载到主模块中。

::

    # all the imports
    import sqlite3
    from flask import Flask, request, session, g, redirect, url_for, \
         abort, render_template, flash

    # configuration
    DATABASE = '/tmp/flaskr.db'
    DEBUG = True
    SECRET_KEY = 'development key'
    USERNAME = 'admin'
    PASSWORD = 'default'

下一步我们要创建真正的应用，然后用同一个文件中的配置来初始化::

    # create our little application :)
    app = Flask(__name__)
    app.config.from_object(__name__)

:meth:`~flask.Config.from_object` 会识别给出的对象（如果是一个字符串，它
会自动导入这个模块），然后查找所有已定义的大写变量。在我们这个例子里，配置
在几行代码前。你也可以把它移动到一个单独的文件中。

从配置文件中读取配置也是一个好方法。:meth:`~flask.Config.from_envvar` 就是
用来做这个事情的::

    app.config.from_envvar('FLASKR_SETTINGS', silent=True)

通过那种方法，就可以设置环境变量 :envvar:`FLASKR_SETTINGS` 来装载指定的配
置文件，装载后会覆盖默认值。silent参数是为了告诉Flask不要报错，即使没有设置
环境变量。

我们需要设置 `secret_key` 来确保客户端Session的安全。合理的设置这个值，而且
越复杂越好。Debug标志用来指示是否开启交互debugger。永远不要在生产环境下开始
debug标志，因为这样会允许用户在服务器上执行代码！

我们还添加了一个方法来快速的连接到指定的数据库。这个方法不仅可以在有用户请
求时打开一个连接,还可以在交互的Python shell和脚本中使用。这对以后会很方便。

::

    def connect_db():
        return sqlite3.connect(app.config['DATABASE'])

最后如果我们想把那个文件当做一个独立的应用来运行，我们需要在文件的末尾加
一行代码来开启服务器 ::

    if __name__ == '__main__':
        app.run()

现在我们应该可以顺利的运行这个应用了。如果你访问服务器，你会得到一个404，
页面没有找到的错误，因为我们还没有创建任何视图。但是我们会在后面再提到它。
首先，我们应该要先让数据库跑起来。

.. admonition:: 让服务器可以被外部访问

   你想然你的服务器被外部访问吗？查看 
   :ref:`externally visible server <public-server>` 部分来获取更多的信息

继续 :ref:`tutorial-dbinit`.
