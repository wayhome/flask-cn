.. _testing:

测试Flask应用程序
==========================

   **物未测，必有漏。**

这句话其实是我瞎掰的说的不一定对, 不过也没有很超过。未经测试的应用程序的代码很难进行改进，且程序员
经常在未经测试的应用程序上面搞很容易抓狂。如果这个应用程序可以自动测试，你就可以安全的作更改且马上
可以知道哪里出了问题。

Flask提供了一种通过暴露Wekzeug测试 :class:`~werkzeug.test.Client` (客户端)且同时处理本地上下文的方法来
替你测试你的应用程序。然后你可以将其应用在你喜欢的测试方式里。在这个文档里，我们将使用 :mod:`unittest` 
包，这个包是随着Python一起已经预安装好的。

要先有应用程序
---------------

首先，我们需要一个应用程序来进行测试；我们将使用 :ref:`tutorial` 作为我们的测试项目。如果你还没有
的话，你可以在 `示例项目`_ 里获取代码。

.. _示例项目:
   http://github.com/mitsuhiko/flask/tree/master/examples/flaskr/

测试骨架
--------------------

为了测试这个项目，我们要新增一个模块 (`flaskr_tests.py`) 。 
且在那里建立一个 unittest 的骨架::

    import os
    import flaskr
    import unittest
    import tempfile

    class FlaskrTestCase(unittest.TestCase):

        def setUp(self):
            self.db_fd, flaskr.app.config['DATABASE'] = tempfile.mkstemp()
            flaskr.app.config['TESTING'] = True
            self.app = flaskr.app.test_client()
            flaskr.init_db()

        def tearDown(self):
            os.close(self.db_fd)
            os.unlink(flaskr.app.config['DATABASE'])

    if __name__ == '__main__':
        unittest.main()

在 :meth:`~unittest.TestCase.setUp` 方法内的代码会建立一个新的测试客户端并且初始化一个新的数据库。此方法会在测试方法执行前先被调用。为了在测试结束删除建立的数据库，我们选择在 :meth:`~unittest.TestCase.tearDown` 方法内关闭并删除这个数据库文件。此外，在准备过程中配置标记将被激活。他的作用是在处理请求时禁用错误捕捉以便于你能在针对应用程序做测试时得到更详细的错误报告。

该测试客户端会提供一个简易的应用程序交互界面。我们可以通过它向应用程序触发测试请求， 测试客户端则会一手掌控所有信息。

由于SQLite3是一个基于文件系统的数据库形式，所以我们可以十分容易地使用临时文件的形式来建立一个临时的数据库并对其进行初始化。方法 :func:`~tempfile.mkstemp` 为我们做了两件事： 他返回了一个低级别的文件句柄和一个随机的文件名，后者就是我们使用的数据库文件名。我们只要保持有 `db_fd` 我们就能使用 :func:`os.close` 方法来关闭该文件。

如果我们现在运行测试套件，我们应该可以看到如下的输出结果::

    $ python flaskr_tests.py

    ----------------------------------------------------------------------
    Ran 0 tests in 0.000s

    OK

尽管这个测试程序没有执行任何的实际测试，但是从这里我们可以看到我们的flaskr程序没有语法错误，否则在引入应用程序类库时就会抛出异常不再执行了。

处女测
--------------

现在是时候来测试应用程序的功能了。我们现在确认一下如果我们访问应用程序的根节点 (``/``)，应用程序应显示 "No entries here so far" 。我们在类里添加了一个新的方法来实现这个功能，如下::

    class FlaskrTestCase(unittest.TestCase):

        def setUp(self):
            self.db_fd, flaskr.app.config['DATABASE'] = tempfile.mkstemp()
            self.app = flaskr.app.test_client()
            flaskr.init_db()

        def tearDown(self):
            os.close(self.db_fd)
            os.unlink(flaskr.DATABASE)

        def test_empty_db(self):
            rv = self.app.get('/')
            assert 'No entries here so far' in rv.data

注意我们的测试方法是以 `test` 开头的；这会让 :mod:`unittest` 模块自动将此方法作为测试方法来执行。

通过使用 `self.app.get` 我们可以把一个HTTP `GET` 请求通过给定的路径发送到应用程序。返回值是一个  :class:`~flask.Flask.response_class` 对象。
我们现在可以用 :attr:`~werkzeug.wrappers.BaseResponse.data` 属性来对应用程序进行核查。对应这个
例子，我们需要核查 ``'No entries here so far'`` 是输出结果的一部分。

再将它执行一次你应该可以看到一次成功的测试结果::

    $ python flaskr_tests.py
    .
    ----------------------------------------------------------------------
    Ran 1 test in 0.034s

    OK

日志的输入输出
------------------

关于这个应用程序，其绝大部分功能是供给管理员使用的，所以我们需要一个途径来记录应用程序运行。为了达到这个
目的，我们向登录和登出页面发送了一些带有表单数据（用户名和密码）的请求。由于登录登出请求会跳转页面，所以
我们告诉客户端要它 `follow_redirects` （跟踪跳转）。

在你的 `FlaskrTestCase` 类里添加如下两个方法::

   def login(self, username, password):
       return self.app.post('/login', data=dict(
           username=username,
           password=password
       ), follow_redirects=True)

   def logout(self):
       return self.app.get('/logout', follow_redirects=True)

现在，我们就可以很方便的通过检查日志查看是否有非法登录的情况。在类里添加一个新的测试方法::

   def test_login_logout(self):
       rv = self.login('admin', 'default')
       assert 'You were logged in' in rv.data
       rv = self.logout()
       assert 'You were logged out' in rv.data
       rv = self.login('adminx', 'default')
       assert 'Invalid username' in rv.data
       rv = self.login('admin', 'defaultx')
       assert 'Invalid password' in rv.data

测试添加功能
--------------------

我们同时还需要测试添加消息的功能是否正常。再添加一个新的测试方法，像这样::

    def test_messages(self):
        self.login('admin', 'default')
        rv = self.app.post('/add', data=dict(
            title='<Hello>',
            text='<strong>HTML</strong> allowed here'
        ), follow_redirects=True)
        assert 'No entries here so far' not in rv.data
        assert '&lt;Hello&gt;' in rv.data
        assert '<strong>HTML</strong> allowed here' in rv.data

这里，我们测试了HTML语法只能在内容里使用，而标题里不行。结果和预想的一样。

运行测试我们应该可以得到三条通过的测试结果::

    $ python flaskr_tests.py
    ...
    ----------------------------------------------------------------------
    Ran 3 tests in 0.332s

    OK

对于那些更复杂的注入带有头和状态代码的测试，你可以在Flask的源码包里找到
`MiniTwit Example`_ 项目，里面有更多更大型的测试用例。


.. _MiniTwit Example:
   http://github.com/mitsuhiko/flask/tree/master/examples/minitwit/


其他测试技巧
--------------------

除了使用上述的测试客户端意外，还可以通过使用方法 :meth:`~flask.Flask.test_request_context` 
，将其和 `with` 语句组合可以产生一个临时的请求上下文。通过此功能你可以像在视图功能里一样访问这些类 :class:`~flask.request`,
:class:`~flask.g` 和 :class:`~flask.session` 。这里有一个使用此方法的完整例子::

    app = flask.Flask(__name__)

    with app.test_request_context('/?name=Peter'):
        assert flask.request.path == '/'
        assert flask.request.args['name'] == 'Peter'

所有其他上下文约束的对象都可以使用相同的方法。

如果你想要在不同的配置环境下测试应用程序，看起来好像没有什么好办法，可以考虑切换到应用程序工厂模式，
(可查阅 :ref:`app-factories`).

注意不管你是否使用测试请求上下文，方法 :meth:`~flask.Flask.before_request` 在方法
:meth:`~flask.Flask.after_request` 被执行之前不一定会被执行。然而方法
:meth:`~flask.Flask.teardown_request` 在测试方法离开 `with` 语块时一定会被执行。  如果你
确实希望方法 :meth:`~flask.Flask.before_request` 也被执行的话, 你需要自行调用
:meth:`~flask.Flask.preprocess_request` 方法::

    app = flask.Flask(__name__)

    with app.test_request_context('/?name=Peter'):
        app.preprocess_request()
        ...

在打开数据库连接或做类似的工作时，这一步就显得十分必要。这取决于你是如何设计你的应用程序的。

保持现场
--------------------------

.. versionadded:: 0.4

有时候我们需要触发一个常规的请求后将上下文现场保持一个较长的时间，以便于触发更多的内部检查。 
有了 Flask 0.4 或以上版本，通过使用方法 :meth:`~flask.Flask.test_client` 
并加上 `with` 语块就可以做到了::

    app = flask.Flask(__name__)

    with app.test_client() as c:
        rv = c.get('/?tequila=42')
        assert request.args['tequila'] == '42'

如果你使用了方法 :meth:`~flask.Flask.test_client` 但是没有加上 `with` 语块, `assert` 语句会报错。
这是因为这里的 `request` 不可用 (因为此操作在在实际请求之外).
不管如何, 记住任何 :meth:`~flask.Flask.after_request` 方法在此时已经被执行，所以你的数据库连接和
其他所有操作可能已经被关闭了。
