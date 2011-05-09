模版
====
:译者: feichao#zoho.com

Flask使用Jinja2作为默认模版。你可以使用任意其他的模版来替代它，但是Flask要求必须安装Jinja2。这是为了能让Flask使用更多的扩展。而这些扩展依赖于Jinja2.

这篇文章只是简单的介绍了Jinja2是如何与Flask相互配合的。如果你想更多的了解Jinja2这个引擎本身，可以去看 `Jinja2模版的官方文档 <http://jinja.pocoo.org/2/documentation/templates>`_

Jinja安装
---------

Flask默认的Jinja配置为：

-	``.html``, ``.htm``, ``.xml``, ``.xhtml`` 文件默认开启自动转义
-	模版文件可以通过 ``{% autoescaping %}`` 标签来选择是否开启自动转义
-	Flask在Jinja2的模版中增加了一些全局变量和辅助方法，它们的值是默认的。

标准上下文
----------
Jinja2的模版默认存在以下全局变量：

.. data:: config
   :noindex:

   当前的configuration对象 (:data:`flask.config`)

   .. versionadded:: 0.6

.. data:: request
   :noindex:

   当前的request对象 (:class:`flask.request`)

.. data:: session
   :noindex:

   当前的session对象 (:class:`flask.session`)

.. data:: g
   :noindex:

   用来保存一个request的全局变量（译者：不同的请求有不同的全局变量，g保存的是当前请求的全局变量） (:data:`flask.g`)

.. function:: url_for
   :noindex:

   :func:`flask.url_for` 函数

.. function:: get_flashed_messages
   :noindex:

   :func:`flask.get_flashed_messages` 函数

.. admonition:: 在Jinja上下文中的行为

	这些变量属于Jinja的上下文变量，而不是普通的全局变量。它们的区别是上下文变量在导入的模版中默认是不可见的。这样做的原因一部分是因为性能的关系，还有一部分是可以让程序更加的清晰。

	对使用者来说，这样有什么区别呢？如果你想导入一个宏，它需要访问request对象，那么有两种方法可以实现：

	1. 	将request对象或request对象的某个属性作为一个参数传给导入的宏。
	2.  "with context" 的方式来导入宏。

	像下面这样导入：

	.. sourcecode:: jinja

		{% from '_helpers.html' import my_macro with context %}

标准过滤器
----------

Jinja2含有如下过滤器（包含了Jinja2模版引擎自带的）：

.. function:: tojson
	:noindex:

	这个函数是用来将对象转换成JSON格式。如果你要实时的生成JavaScript，那么这个功能是非常实用的。
	要注意不能在 `script` 标签里面进行转义。所以如果你想在 `script` 标签里面使用这个函数，要确保用 ``|safe`` 来关闭自动转义：

	.. sourcecode:: html+jinja

		<script type=text/javascript>
			doSomethingWith({{ user.username|tojson|safe }});
		</script>

	``|tojson`` 过滤器会自动转义前置的斜杠。

控制自动转义
------------

自动转义就是自动帮你将特殊的字符替换成转义符号。HTML（或者XML， XHTML）的特殊字符有 ``&``, ``>``, ``<``, ``"``, ``'`` 。因为这些字符在文档中有它自己特殊的含义，所以如果你想在文章中使用这些符号，必须将它替换成转义符号。如果不这样做，不仅用户使用不了这些符号，还会导致安全问题。(更多 :ref:`xss`)

但是有时候你需要在模版中禁用自动转义。如果你想直接将HTML插入页面，比如将markdown语言转换成HTML，那么你就需要这样做了。

有3种方法可以关闭自动转义：

-	在Python文件中进行转义。先在 :class:`~flask.Markup` 对象中进行转义，然后将它传送给模版。一般推荐使用这个方式。
- 	在模版文件中进行转义。通过 ``|safe`` 过滤器来表示字符串是安全的(``{{ myvariable|safe }}``)
- 	暂时禁用全局的自动转义功能。

要想在模版中禁用全局自动转义功能，可以用 ``{% autoescaping %}`` 语句块:

.. sourcecode:: html+jinja

	{% autoescaping false %}
		<p>autoescaping is disableed here
		<p>{{ will_not_be_escaped }}
	{% endautoescape %}

在这么做的时候，要语句块中使用到的变量非常小心。

引入过滤器
----------

如果你想在Jinja2中引入你自己的过滤器，有2种方法可以做到。你可以把他们放在某个应用的
:attr:`~flask.Flask.jinja_env` 对象里面或者用
:meth:`~flask.Flask.template_filter` 装饰器。

下面的两个例子都把对象的元素颠倒过来 ::

    @app.template_filter('reverse')
    def reverse_filter(s):
        return s[::-1]

    def reverse_filter(s):
        return s[::-1]
    app.jinja_env.filters['reverse'] = reverse_filter

在装饰器里，如果你想用函数的名字来做装饰器的名字，那么装饰器参数可以省略。

上下文处理器
-------------

Flask中的上下文处理器是为了把新的变量自动插入到模版的上下文。上下文处理器在模版被呈现之前运行，它可以把新的值插入到模版中。上下文处理器是一个返回一个字典的函数。字典的键名和键值会与模版中想对应的变量的进行合并 ::

	@app.context_processor
	def inject_user():
		return dict(user=g.user)

上面的上下文处理器在模版创建了一个 `user` 的变量，它的值是 `g.user` 。这个例子不是很实用，因为 `g` 变量在模版中总是可以访问的，但是它展示了上下文处理器的使用方法。
