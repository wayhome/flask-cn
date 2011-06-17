.. _tutorial-templates:

第六步: 模版
=====================

现在我们可以开始制作我们的网页模版了。如果我们现在访问URL，我们会得到一个
“Flask无法找到模版文件”的异常。我们的模版将使用 `Jinja2`_ 的格式，而且默
认是打开自动转义的。这也就是说，除非我们在代码中用 :class:`~flask.Markup` 
标记一个值，或者在模版中用 ``|safe`` 过滤器，否则Jinja2会将一些特殊字符，
如 ``<`` 或 ``>`` 用XML格式来转义。

我们将使用模版继承机制来使所有的页面使用同一个布局。

把以下的模版放在 `template` 目录下：

.. _Jinja2: http://jinja.pocoo.org/2/documentation/templates

layout.html
-----------

这个模版包含了HTML的主要结构，标题和一个登陆的链接（或者登出如果用户已经登
陆）。它还负责显示flashed messages。 ``{% block body %}`` 可以被子模版的相
同名字（ ``body`` )的结构所替换

:class:`~flask.session` 字典在模版中也是可以访问的。所以你可以用session来
检查用户是否已登陆。注意在Jinja中，你可以访问对象或字典的未使用过的属性和
成员。就如下面的代码一样，即使session中没有 ``'logged_in'`` :

.. sourcecode:: html+jinja

    <!doctype html>
    <title>Flaskr</title>
    <link rel=stylesheet type=text/css href="{{ url_for('static', filename='style.css') }}">
    <div class=page>
      <h1>Flaskr</h1>
      <div class=metanav>
      {% if not session.logged_in %}
        <a href="{{ url_for('login') }}">log in</a>
      {% else %}
        <a href="{{ url_for('logout') }}">log out</a>
      {% endif %}
      </div>
      {% for message in get_flashed_messages() %}
        <div class=flash>{{ message }}</div>
      {% endfor %}
      {% block body %}{% endblock %}
    </div>

show_entries.html
-----------------

这个模版继承自上面的 `layout.html` ,来显示文章。 `for` 循环遍历所有的文章。
我们通过 :func:`~flask.render_template` 来传入参数。我们还告诉表单使用 
`HTTP` 的 `POST` 方法提交到 `add_entry` 函数:

.. sourcecode:: html+jinja

    {% extends "layout.html" %}
    {% block body %}
      {% if session.logged_in %}
        <form action="{{ url_for('add_entry') }}" method=post class=add-entry>
          <dl>
            <dt>Title:
            <dd><input type=text size=30 name=title>
            <dt>Text:
            <dd><textarea name=text rows=5 cols=40></textarea>
            <dd><input type=submit value=Share>
          </dl>
        </form>
      {% endif %}
      <ul class=entries>
      {% for entry in entries %}
        <li><h2>{{ entry.title }}</h2>{{ entry.text|safe }}
      {% else %}
        <li><em>Unbelievable.  No entries here so far</em>
      {% endfor %}
      </ul>
    {% endblock %}

login.html
----------

最后是登陆页面的模版。它仅仅是显示一个表单来允许用户登陆：

.. sourcecode:: html+jinja

    {% extends "layout.html" %}
    {% block body %}
      <h2>Login</h2>
      {% if error %}<p class=error><strong>Error:</strong> {{ error }}{% endif %}
      <form action="{{ url_for('login') }}" method=post>
        <dl>
          <dt>Username:
          <dd><input type=text name=username>
          <dt>Password:
          <dd><input type=password name=password>
          <dd><input type=submit value=Login>
        </dl>
      </form>
    {% endblock %}

继续 :ref:`tutorial-css`.
