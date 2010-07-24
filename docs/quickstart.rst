.. _quickstart:

快速上手
==========

急于开始了吗?本文就如何上手Flask提供了一个很好的介绍.
假定你已经安装好了Flask.如果没有的话，请参考 :ref:`installation` 这一节.


一个最小的应用
---------------------

一个最小的Flask应用程序看起来像是这样::

    from flask import Flask
    app = Flask(__name__)

    @app.route('/')
    def hello_world():
        return "Hello World!"

    if __name__ == '__main__':
        app.run()

把它存为 `hello.py` 或其它相似的文件名，然后用python解释器运行这个文件.
请确保你的程序名不是叫做 `flask.py` ,因为这样会和Flask本身发生冲突.

::

    $ python hello.py
     * Running on http://127.0.0.1:5000/

把浏览器指向 `http://127.0.0.1:5000/ <http://127.0.0.1:5000/>`_, 你将看到
你的 hello world的问候.

那么这段代码到底做了什么?

1. 首先我们导入了 :class:`~flask.Flask` 类.这个类的一个实例将会是我们的
   WSGI程序.
2. 接下来我实们来例化这个类.我们把模块/包的名字传给它,这样Flask就会知道它
   将要到哪里寻找模板，静态文件之类的东西.
3. 然后我们使用 :meth:`~flask.Flask.route` 装饰器告诉Flask哪个网址将会触发
   我们的函数.
4. 这个函数还有一个作用是为特定的函数生成网址，并返回我们想要显示在用户浏
   览器的信息.
5. 最后我们用 :meth:`~flask.Flask.run` 函数来运行本地服务器以及我们的应用.
   ``if __name__ == '__main__':`` 确保了服务器只会在直接用Python解释器执行
   该脚本的时候运行,而不会在导入模块的时候运行.

要停止服务器，按 Ctrl+C.

.. _public-server:

.. admonition:: 外部可见的服务器

   当你运行服务器时你可能会注意到该服务器仅能从你自己的电脑访问，网络中的
   其它地方都将不能访问.这是因为默认启用的调试模式中，应用程序的用户可以执
   行你的电脑上的任意Python代码。如果你禁用了 `调试` 或者信任你所在的网络
   中的用户，你可以使你的服务器公开可访问.

   只需要像这样更改 :meth:`~flask.Flask.run` 方法 ::

       app.run(host='0.0.0.0')

   这样告诉了你的操作系统去监听一个公开的IP.


调试模式
----------

虽然 :meth:`~flask.Flask.run` 方法很适于启动一个本地的测试服务器,
但是你每次修改代码后都得重启它.这样显然不好,Flask当然可以做得更好.
如果你开启服务器的debug支持,那么每次代码更改后服务器都会自动重启，
如果出现问题的话，还会提供给你一个有用的调试器.


有两种方法来开启debug模式.你可以在application对象上设置标志位 ::

    app.debug = True
    app.run()

或者作为run方法的一个参数传入 ::

    app.run(debug=True)

两者均有完全相同的效果.

.. admonition:: 注意事项

   交互调试器不能在forking环境下工作，因此很少有可能将它用于产品服务器.
   并且调试器仍然可以执行任意的代码，这是一个重大的安全风险，
   因此 **绝不能用于生产机器** .
   

运行中的调试器的截图:

.. image:: _static/debugger.png
   :align: center
   :class: screenshot
   :alt: screenshot of debugger in action


路由
-------

正如你看到的，:meth:`~flask.Flask.route` 装饰器用于绑定一个函数到一个网址.
但是它不仅仅只有这些!你可以构造动态的网址并给函数附加多个规则.

这里是一些例子 ::

    @app.route('/')
    def index():
        return 'Index Page'

    @app.route('/hello')
    def hello():
        return 'Hello World'


变量规则
``````````````

现代的web应用程序有着一些漂亮的网址.这有助于用户记住网址，尤其是对于那些
来自较慢的网络连接的移动设备的用户显的很贴心.如果用户能直接访问他所想要
的页面，而不必每次都从首页找起，那么用户可能会更喜欢这个网页，下次更愿意
回来.

要向URL中添加变量部分，你可以标记这些特殊的字段为 ``<variable_name>``.
然后这个部分就可以作为参数传给你的函数.rule可以指定一个可选的转换器
像这样 ``<converter:variable_name>``.这里有一些例子::

    @app.route('/user/<username>')
    def show_user_profile(username):
        # show the user profile for that user
        pass

    @app.route('/post/<int:post_id>')
    def show_post(post_id):
        # show the post with the given id, the id is an integer
        pass

目前有以下转换器存在:

=========== ===========================================
`int`       接受整数
`float`     接受浮点数类型
`path`      和默认的行为类似，但也接受斜线
=========== ===========================================

.. admonition:: 唯一的网址 / 重定向行为

   Flask的网址规则是基于Werkzeug的routing模块.这个模块背后的思想是确保
   好看以及唯一的网址，基于Apache和一些创建较早的服务器.

   以如下两个规则为例 ::

        @app.route('/projects/')
        def projects():
            pass

        @app.route('/about')
        def about():
            pass

   他们看起来相似，不同在于网址 *定义* 中结尾的斜线.第一种情况是规范网址
   `projects` 端点有一个斜线. 从这种意义上讲，和文件夹有些类似.访问没有
   斜线的网址会被Flask重定向到带有斜线的规范网址去.

   然而在第二种情况下的网址的定义没有斜线，这种行为类似于访问一个文件，
   访问一个带斜线的网址将会是一个404错误.

   为什么这样做?用户访问网页的时候可能会忘记了斜线，这样可以使得相关的网
   址能继续工作.这种行为和Apache以及其它服务器工作方式类似.另外网址保持唯
   一有助于搜索引擎不会索引同一页面两次.

.. _url-building:

构建URL
````````````

如果它能匹配网址，那么从它是否能生成网址呢? 你当然可以! 为一个特定的函数
构建网址，你可以使用 :func:`~flask.url_for` 函数.它接受函数名作为第一个
参数，还有一些关键字参数，每个对应于网址规则中的一个变量部分.未知的变量
部分将附加到网址后面作为查询参数，这里有一些例子:

>>> from flask import Flask, url_for
>>> app = Flask(__name__)
>>> @app.route('/')
... def index(): pass
... 
>>> @app.route('/login')
... def login(): pass
... 
>>> @app.route('/user/<username>')
... def profile(username): pass
... 
>>> with app.test_request_context():
...  print url_for('index')
...  print url_for('login')
...  print url_for('login', next='/')
...  print url_for('profile', username='John Doe')
... 
/
/login
/login?next=/
/user/John%20Doe

(这里用到了 :meth:`~flask.Flask.test_request_context` 函数,它主要是告
诉Flask我们正在处理一个request,即使我们不是，我们在一个交互式的Python
shell下.更进一步参考 :ref:`context-locals`).

为什么你想要构建网址，而不是在模板里面硬编码? 这里有三个很好的理由:

1. 反向解析比硬编码网址更具有描述性.而且当你只在一个地方更改网址，而不用
   满世界的更改网址时，这就显得更重要了.
2. 网址构建过程会自动的为你处理特殊字符和unicode数据转义，这些对你而已都
   是透明的，你不必面对这一切.
3. 如果你的应用程序位于根路径以外的地方(比如在 ``/myapplication`` 而不是
   ``/``), :func:`~flask.url_for` 将妥善的为你处理好这些.


HTTP 方法
````````````

HTTP (web应用程序的会话协议) 知道访问网址的不同方法.默认情况下路由只回
应 `GET` 请求,但是通过 :meth:`~flask.Flask.route` 装饰器提供的 `methods`
参数你可以更改这个行为.这里有一些例子::

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            do_the_login()
        else:
            show_the_login_form()

如果当前是 `GET`, `HEAD` 也会自动的为你添加.你不必处理它.它确保 `HEAD` 
请求按照 `HTTP RFC`_ (描述HTTP协议的文档) 要求的那样来处理.所以你可以
完全的忽略这部分HTTP规范.

你不清楚什么是一个HTTP方法? 没关系，这里对它们做一个快速介绍:

The HTTP method (also often called "the verb") tells the server what the
clients wants to *do* with the requested page.  The following methods are
very common:

`GET`
    The Browser tells the server: just *get* me the information stored on
    that page and send them to me.  This is probably the most common
    method.

`HEAD`
    The Browser tells the server: get me the information, but I am only
    interested in the *headers*, not the content of the page.  An
    application is supposed to handle that as if a `GET` request was
    received but not deliver the actual contents.  In Flask you don't have
    to deal with that at all, the underlying Werkzeug library handles that
    for you.

`POST`
    The browser tells the server that it wants to *post* some new
    information to that URL and that the server must ensure the data is
    stored and only stored once.  This is how HTML forms are usually
    transmitting data to the server.

`PUT`
    Similar to `POST` but the server might trigger the store procedure
    multiple times by overwriting the old values more than once.  Now you
    might be asking why this is any useful, but there are some good
    reasons to do that.  Consider the connection is lost during
    transmission, in that situation a system between the browser and the
    server might sent the request safely a second time without breaking
    things.  With `POST` that would not be possible because it must only
    be triggered once.

`DELETE`
    Remove the information that the given location.

`OPTIONS`
    Provides a quick way for a requesting client to figure out which
    methods are supported by this URL.  Starting with Flask 0.6, this
    is implemented for you automatically.

Now the interesting part is that in HTML4 and XHTML1, the only methods a
form might submit to the server are `GET` and `POST`.  But with JavaScript
and future HTML standards you can use other methods as well.  Furthermore
HTTP became quite popular lately and there are more things than browsers
that are speaking HTTP.  (Your revision control system for instance might
speak HTTP)

.. _HTTP RFC: http://www.ietf.org/rfc/rfc2068.txt

静态文件
------------

动态的web应用程序也需要静态文件.这往往是CSS和JavaScript文件的来源.理想情况
下你的web服务器配置好了为你服务它们，但在开发过程中Flask也可以为你做这些.
只需要在你的包或者模块旁边里创建一个名为 `static` 的文件夹，它将可以通过
`/static` 来访问.

要生成这部分的网址，使用特殊的 ``'static'`` 网址名字 ::

    url_for('static', filename='style.css')

这个文件将位于文件系统的 ``static/style.css`` 位置.

模板渲染
-------------------

从Python生成HTML不好玩也相当麻烦,因为你必须自己做HTML转义以保证应用
程序的安全.因为这个原因，Flask自动为您配置了 `Jinja2 <http://jinja.pocoo.org/2/>`_
模板引擎.

你可以使用 :func:`~flask.render_template` 来渲染模板.所有您需要做的
是提供模板的名字，以及你想要作为参数传给模板引擎的变量.这里是一个如
和渲染模板的简单例子::

    from flask import render_template

    @app.route('/hello/')
    @app.route('/hello/<name>')
    def hello(name=None):
        return render_template('hello.html', name=name)

Flask将会在 `templates` 文件夹下查找模板.因此如果你的应用程序是一个
模块，这个文件夹在那个模块的旁边，或者如果它实际上是一个包含在您的
包里面的包:

**案例 一**: 一个模块 ::
    
    /application.py
    /templates
        /hello.html

**案例 二**: 一个包::

    /application
        /__init__.py
        /templates
            /hello.html

作为模板来讲你可以充分利用Jinja2模板的威力.前往 文档的 :ref:`templating`
章节或者 `Jinja2 模板文档 <http://jinja.pocoo.org/2/documentation/templates>`_ 
查看更多信息.

这里是一个模版的例子:

.. sourcecode:: html+jinja

    <!doctype html>
    <title>Hello from Flask</title>
    {% if name %}
      <h1>Hello {{ name }}!</h1>
    {% else %}
      <h1>Hello World!</h1>
    {% endif %}

在模板内部你可以访问 :class:`~flask.request`, :class:`~flask.session`
和 :class:`~flask.g` [#]_ 对象,以及 :func:`~flask.get_flashed_messages`
函数.

当使用继承的时候模板显得特别有用.如果你想了解继承是如何工作的，请查看
:ref:`template-inheritance` 模式文档.基本上模板继承可以使得特定元素在
每个页面上都显示(比如header,navigation和footer).

自动转义默认是开启的，所以如果名字中包含HTML将被自动转义.如果你信任一个
变量并知道它是安全的(例如来自于一个把wiki标记转换为HTML格式的模板),你可以
使用类 :class:`~jinja2.Markup` 或者 模板中的 ``|safe`` 标签，来标记它是
安全的. 前往Jinja2文档查看更多的例子.

这里就 :class:`~jinja2.Markup` 类如何工作有一个简单的介绍:

>>> from flask import Markup
>>> Markup('<strong>Hello %s!</strong>') % '<blink>hacker</blink>'
Markup(u'<strong>Hello &lt;blink&gt;hacker&lt;/blink&gt;!</strong>')
>>> Markup.escape('<blink>hacker</blink>')
Markup(u'&lt;blink&gt;hacker&lt;/blink&gt;')
>>> Markup('<em>Marked up</em> &raquo; HTML').striptags()
u'Marked up \xbb HTML'

.. versionchanged:: 0.5

   自动转义不再为所有的模板开启.如下扩展名的模板会触发自动转义: ``.html``,
   ``.htm``,``.xml``, ``.xhtml``.从字符串加载的模板将禁用自动转义.

.. [#] 不确定 :class:`~flask.g` 对象是什么? 它就是你可以用来存储信息的
   某个东西,查看对象 (:class:`~flask.g`) 和 :ref:`sqlite3` 的文档以得到
   更多信息.


访问 Request 数据
----------------------

对web应用程序来说最重要的就是对客户端发送到服务器端的数据做出响应.在
Flask中这个信息由一个全局的 :class:`~flask.request` 对象提供.如果你
有一些Python的经验，你可能会奇怪这个对象怎么可能是全局的，并且Flask
怎么还能依然线程安全. 答案是局部上下文.


.. _context-locals:

局部上下文
``````````````

.. admonition:: 内幕信息

   如果你想理解它是怎么工作的，你怎么用它来做测试,那么继续读下去,
   否则跳过这节.

Flask中的某些对象是全局对象,但它不是一个标准的全局对象，实际上是一个
本地对象的代理.听起来真拗口.但实际上却很容易理解.


想象一下正在处理线程的上下文.当一个请求进来，web服务器决定生成一个新的
线程或别的东西时，这个基本对象能够很好的胜任处理其它并发系统不仅仅是线
程.当Flask开始内部的线程处理时，它把当前线程当作活动上下文并把当前应用
程序和WSGI环境绑定到这个上下文(线程).它以一种智能的方式使得在一个应用程序
中能调用另一个应用程序而不会中断.

那么这对你而言意味着什么?除非你在做单元测试或一些不同的东西，基本上你可
以完全忽略这种情况.你将发现依赖于一个request对象的代码会突然挂掉，因为
那里并没有request对象.解决方案就是创建一个request对象并把它绑定到上下文.
在单元测试中最早的解决方案是使用 :meth:`~flask.Flask.test_request_context`
上下文管理器.结合 `with` 声明它将绑定一个测试request，以便于你交互.这里
是一个例子::

    from flask import request

    with app.test_request_context('/hello', method='POST'):
        # now you can do something with the request until the
        # end of the with block, such as basic assertions:
        assert request.path == '/hello'
        assert request.method == 'POST'

另一个可能性是传递一个完整的WSGI环境给:meth:`~flask.Flask.request_context` 
方法::

    from flask import request

    with app.request_context(environ):
        assert request.method == 'POST'

Request 对象
``````````````````

在API章节对request有着详尽的文档描述，所以我们这里不会深入讲解
(查看 :class:`~flask.request`).这里仅仅提一下一些最常见的操作.
首先你要做的是从 `flask` 导入它::

    from flask import request

当前的request方法可以通过 :attr:`~flask.request.method` 属性获得.
要访问表单数据(由 `POST` 或者 `PUT` 请求传递的数据),可以通过
:attr:`~flask.request.form` 属性得到.这里有一个关于上诉提到的
两个属性的完整的例子::

    @app.route('/login', methods=['POST', 'GET'])
    def login():
        error = None
        if request.method == 'POST':
            if valid_login(request.form['username'],
                           request.form['password']):
                return log_the_user_in(request.form['username'])
            else:
                error = 'Invalid username/password'
        # this is executed if the request method was GET or the
        # credentials were invalid

如果 `form` 属性中不存在这个键会发生什么?在这种情况下将会抛出 :exc:`KeyError`.
你可以像捕捉标准错误一样捕捉它，但如果你不这样做，将会显示给你一个 HTTP 400 Bad
Request页面.因此很多情况下你不必处理这个问题.

要访问诸如(``?key=value``)之类形式的网址所提交的参数，你可以使用 :attr:
`~flask.request.args` 属性::

    searchword = request.args.get('q', '')

我们推荐使用 `get` 访问网址参数或者捕捉 `KeyError`,因为用户可能更改网址，
展现给他们一个 400 bad request 页面不够友好.

如果要得到关于该对象的方法和属性的一份全面的列表，查看文档 :class:`~flask.request` .


文件上传
````````````

用Flask处理文件上传很容易.你只要确保不要忘记在你的HTML表单设置属性
``enctype="multipart/form-data"`` ，否则浏览器根本不会提交你的文件.

上传的文件储存在内存或者文件系统中的一个临时位置.你可以通过request
对象的 :attr:`~flask.request.files` 属性来访问这些文件.每个上传的
文件都储存在那个字典里.它表现的就像一个标准的Python :class:`file`
对象,但它还有一个 :meth:`~werkzeug.FileStorage.save`  方法允许你
把文件存储在服务器的文件系统上.这里有一个它如何工作的例子::

    from flask import request

    @app.route('/upload', methods=['GET', 'POST'])
    def upload_file():
        if request.method == 'POST':
            f = request.files['the_file']
            f.save('/var/www/uploads/uploaded_file.txt')
        ...

如果你想知道客户端把文件上传到你的应用之前时的文件命名,你可以访问
:attr:`~werkzeug.FileStorage.filename` 属性.但请牢牢记住，这个值
是可以伪造的，永远不要信任这个值.如果你想使用客户端的文件名把文件
存在服务器，你可以把它传递给Werkzeug提供给你的 
:func:`~werkzeug.secure_filename` 函数::

    from flask import request
    from werkzeug import secure_filename

    @app.route('/upload', methods=['GET', 'POST'])
    def upload_file():
        if request.method == 'POST':
            f = request.files['the_file']
            f.save('/var/www/uploads/' + secure_filename(f.filename))
        ...

更多例子请查看 :ref:`uploading-files` 模式.

Cookies
```````

访问cookies你可以使用 :attr:`~flask.request.cookies` 属性.这也是
一个字典，包含了客户端传输的所有的cookies.如果你想使用会话而不想
直接使用cookies的话请参考 :ref:`sessions` 章节,它在cookies的基础
上增加了一些安全措施.


跳转和错误
--------------------

To redirect a user to somewhere else you can use the
:func:`~flask.redirect` function, to abort a request early with an error
code the :func:`~flask.abort` function.  Here an example how this works::

    from flask import abort, redirect, url_for

    @app.route('/')
    def index():
        return redirect(url_for('login'))

    @app.route('/login')
    def login():
        abort(401)
        this_is_never_executed()

This is a rather pointless example because a user will be redirected from
the index to a page he cannot access (401 means access denied) but it
shows how that works.

By default a black and white error page is shown for each error code.  If
you want to customize the error page, you can use the
:meth:`~flask.Flask.errorhandler` decorator::

    from flask import render_template

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('page_not_found.html'), 404

Note the ``404`` after the :func:`~flask.render_template` call.  This
tells Flask that the status code of that page should be 404 which means
not found.  By default 200 is assumed which translates to: all went well.

.. _sessions:

会话
--------

Besides the request object there is also a second object called
:class:`~flask.session` that allows you to store information specific to a
user from one request to the next.  This is implemented on top of cookies
for you and signs the cookies cryptographically.  What this means is that
the user could look at the contents of your cookie but not modify it,
unless he knows the secret key used for signing.

In order to use sessions you have to set a secret key.  Here is how
sessions work::

    from flask import Flask, session, redirect, url_for, escape, request
    
    app = Flask(__name__)

    @app.route('/')
    def index():
        if 'username' in session:
            return 'Logged in as %s' % escape(session['username'])
        return 'You are not logged in'

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        if request.method == 'POST':
            session['username'] = request.form['username']
            return redirect(url_for('index'))
        return '''
            <form action="" method="post">
                <p><input type=text name=username>
                <p><input type=submit value=Login>
            </form>
        '''

    @app.route('/logout')
    def logout():
        # remove the username from the session if its there
        session.pop('username', None)
        return redirect(url_for('index'))

    # set the secret key.  keep this really secret:
    app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

The here mentioned :func:`~flask.escape` does escaping for you if you are
not using the template engine (like in this example).

.. admonition:: How to generate good Secret Keys

   The problem with random is that it's hard to judge what random is.  And
   a secret key should be as random as possible.  Your operating system
   has ways to generate pretty random stuff based on a cryptographic
   random generator which can be used to get such a key:

   >>> import os
   >>> os.urandom(24)
   '\xfd{H\xe5<\x95\xf9\xe3\x96.5\xd1\x01O<!\xd5\xa2\xa0\x9fR"\xa1\xa8'

   Just take that thing and copy/paste it into your code and you're done.

消息闪烁
----------------

Good applications and user interfaces are all about feedback.  If the user
does not get enough feedback he will probably end up hating the
application.  Flask provides a really simple way to give feedback to a
user with the flashing system.  The flashing system basically makes it
possible to record a message at the end of a request and access it next
request and only next request.  This is usually combined with a layout
template that does this.

To flash a message use the :func:`~flask.flash` method, to get hold of the
messages you can use :func:`~flask.get_flashed_messages` which is also
available in the templates.  Check out the :ref:`message-flashing-pattern`
for a full example.

日志记录
----------

.. versionadded:: 0.3

Sometimes you might be in the situation where you deal with data that
should be correct, but actually is not.  For example you have some client
side code that sends an HTTP request to the server, and it's obviously
malformed.  This might be caused by a user tempering with the data, or the
client code failed.  Most the time, it's okay to reply with ``400 Bad
Request`` in that situation, but other times it is not and the code has to
continue working.

Yet you want to log that something fishy happened.  This is where loggers
come in handy.  As of Flask 0.3 a logger is preconfigured for you to use.

Here are some example log calls::

    app.logger.debug('A value for debugging')
    app.logger.warning('A warning occurred (%d apples)', 42)
    app.logger.error('An error occurred')

The attached :attr:`~flask.Flask.logger` is a standard logging
:class:`~logging.Logger`, so head over to the official stdlib
documentation for more information.

WSGI 中间件集成
---------------------------

If you want to add a WSGI middleware to your application you can wrap the
internal WSGI application.  For example if you want to use one of the
middlewares from the Werkzeug package to work around bugs in lighttpd, you
can do it like this::

    from werkzeug.contrib.fixers import LighttpdCGIRootFix
    app.wsgi_app = LighttpdCGIRootFix(app.wsgi_app)
