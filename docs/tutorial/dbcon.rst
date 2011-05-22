.. _tutorial-dbcon:

第四步：请求数据库连接
----------------------

现在，我们知道了如何来创建一个数据库连接，如何来执行脚本，但是我们如何能优
雅的为每一次的请求创建连接？数据库连接在所以的函数中都是需要的，所以能自动
在请求之前初始化，请求结束后关闭就显得很有意义。

Flask提供了 :meth:`~flask.Flask.after_request` 和
:meth:`~flask.Flask.before_request` 装饰器来让我们做到这一点::

    @app.before_request
    def before_request():
        g.db = connect_db()

    @app.after_request
    def after_request(response):
        g.db.close()
        return response

用 :meth:`~flask.Flask.before_request` 装饰的函数在每次请求之前
被调用，它没有参数。用 :meth:`~flask.Flask.after_request` 装饰的函数是在每
次请求结束后被调用，而且它需要传入response。这类函数必须返回同一个response
对象或者一个不同的response对象。在这里，我们不对response做修改，返回同一个
对象。

我们把当前的数据库连接保存在一个特殊的对象 :data:`~flask.g` 里面，这个对象
flask已经为我们提供了。这个对象只能用来为一个请求保存信息，每一个函数都可以
访问这个对象。不要用其他的对象来保存信息，因为在多线程的环境下会无法工作。
:data:`~flask.g` 对象是一个特殊的对象，它会在后台做一些魔术来确保它能够跟我
们预想的一样执行。

继续 :ref:`tutorial-views`.
