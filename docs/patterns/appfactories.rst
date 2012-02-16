.. _app-factories:

应用程序的工厂模式
=====================

如果你已经在你的应用里使用了包和蓝图 (:ref:`blueprints`) 的话，实际上还有许多种非常好的方法让你更爽。一般的做法是在import蓝图后紧接着创建应用程序对象。但是如果将应用程序对象创建过程移到某个方法内，那么你就可以随时地创建应用程序对象的各种实例了。

你估计会问，为什么我要这么干？

1.  为了测试。这样每一种配置设定，你都可以创建基于该配置的应用实例。
2.  多个实例。想象一下你需要运行同一个应用的不同版本。当然你也可以在你的web服务器上做和多类似的配置以实现这个目的，但是如果你用了工厂，即使要在一个应用线程下同时运行同一个应用的不同实例也不会让你无从下手。

那么该如何实现呢?

一个基本的工厂
---------------

也就是说在方法里配置应用程序，就像这样::

    def create_app(config_filename):
        app = Flask(__name__)
        app.config.from_pyfile(config_filename)

        from yourapplication.views.admin import admin
        from yourapplication.views.frontend import frontend
        app.register_blueprint(admin)
        app.register_blueprint(frontend)

        return app

这么做的不足之处是你不能在import蓝图后在蓝图内调用应用程序对象。但是你也可以在一个请求里面调用它。怎么拿到应用程序的当前配置呢？使用 :data:`~flask.current_app`::

    from flask import current_app, Blueprint, render_template
    admin = Blueprint('admin', __name__, url_prefix='/admin')

    @admin.route('/')
    def index():
        return render_template(current_app.config['INDEX_TEMPLATE'])

在上述例子中，我们尝试了在当前配置里查一个模板的名称。

使用应用程序
------------------

要使用应用程序我们就必须先创建它。如下面的例子所示，有一个  `run.py` 文件负责执行应用::

    from yourapplication import create_app
    app = create_app('/path/to/config.cfg')
    app.run()

更好的工厂
--------------------

上面提到的工厂方法内容还是有点蠢，你还可以对它继续改进。以下就是一些既简单又可行的方法:

1.  让单元测试接受配置变量变得可行，这样一来你就不用在文件系统内单独开辟配置文件了。
2.  在应用执行的同时调用蓝图里的某一个方法，这样你就有地方修改应用的一些特性（比如挂上诸如before / after request handlers（请求前/后执行者）的操作）。
3.  如果需要的话，可以在创建应用时添加WSGI中间件。
