.. _larger-applications:

更大的应用
===================

对于更大的应用而言，使用包来代替模块是一个不错的选择。而且它也十分方便，试想一下一个小的应用就像这样::

    /yourapplication
        /yourapplication.py
        /static
            /style.css
        /templates
            layout.html
            index.html
            login.html
            ...

简单的包
---------------

要把它变成大型项目，只要在已有的项目根目录下建立再创建一个 `yourapplication` 目录，然后把原根目录下所有的东西都移到这个新建目录里面，然后将 `yourapplication.py` 重命名为 `__init__.py` 就好了。（请确认要事先删除所有 `.pyc` 文件，否则程序很有可能会挂）

你应该看到的是如下的结构::

    /yourapplication
        /yourapplication
            /__init__.py
            /static
                /style.css
            /templates
                layout.html
                index.html
                login.html
                ...

但是这样的话我们怎么让应用跑起来呢？直接执行 ``python yourapplication/__init__.py`` 是不行的。因为Python的设计者并不希望包内的模块成为一个启动文件。不过这个问题不大，只要再创建一个名为 `runserver.py` ，使其与里面的 `yourapplication` 在同一级，然后在里面添加如下内容::

    from yourapplication import app
    app.run(debug=True)

我们这么做是为了什么呢？这意味着现在我们可以将原来一个单独的应用重构为许多模块拼接而成。你只需要记住要遵循如下的准则:

1. `Flask` 应用对象的创建必须放在 `__init__.py` 文件内。只有这样每个模块才能安全的import（引入）它，且 `__name__` 变量才能解析到正确的包。
2. 所有的view（视图）方法（指那些在头上有 :meth:`~flask.Flask.route` 修饰的方法）必须放在 `__init__.py` 文件里import。并在 **应用程序对象创建后** 在模块被调用的地方，而不是他自身所在位置import view模块。

请看示例 `__init__.py`::

    from flask import Flask
    app = Flask(__name__)

    import yourapplication.views

这是一个 `views.py` 的例子::

    from yourapplication import app

    @app.route('/')
    def index():
        return 'Hello World!'

然后你应该的项目结构应该像这样::

    /yourapplication
        /yourapplication
            /__init__.py
            /views.py
            /static
                /style.css
            /templates
                layout.html
                index.html
                login.html
                ...

.. admonition:: 回环Imports（引入）

   每个Python程序员都痛恨这个问题，不过我们还是加了这个功能:
   回环Imports （意思是说有两个模块互相依赖。在上述例子中 `views.py` 依赖于 `__init__.py` ）。要注意在通常情况下这是很危险的做法，不过在这里问题还不大。这是因为我们不会在 `__init__.py` 里面使用视图，我们只是需要确认模块是否被引入而且我们是在文件的最后做这件事的。

   不过即使这么做还是会导致一些问题的产生。什么？除了这个你还要上修饰？那根本是行不通的。你还是去看看 :ref:`becomingbig` 这一节试试能不能给你点别的灵感吧。


.. _working-with-modules:

使用Blueprints（蓝图）
-----------------------

如果你要做一个大家伙，我们十分建议你将它先分成许多小的组，每个组由一个blueprint（蓝图）协助实现。如果你需要了解有关于此的详细内容，请查阅文档内的 :ref:`blueprints` 章节。
