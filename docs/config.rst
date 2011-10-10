.. _config:

配置管理
======================
:译者: G_will@ieqi.com

网络应用总是需要一些配置。\
有些东西你可能需要做一些更改、配置，\
比如，切换debug模式、变更密钥，还有一些其他类似的东西。

通常在Flask中，在应用启动的时候就需要载入配置。\
对于一些小的应用，你可以将配置硬编码到网站应用源代码中，不过也有更好的方法。

不同于通常的配置载入方式，在Flask中，有一个现成的保存、载入的对象，\
就是 :class:`~flask.Flask` 类中的 :attr:`~flask.Flask.config` 对象。\
在这个对象中Flask不仅存放自己的配置，还存放拓展插件的配置，而且也存放\
你对于自己应用的自己的配置。

基本配置
--------------------

:attr:`~flask.Flask.config` 实际上继承于字典（dictionary）类型，所以你可以像操作任何字典那样配置它：
::

    app = Flask(__name__)
    app.config['DEBUG'] = True

配置好的配置参数值也被包含在 :attr:`~flask.Flask` 对象中，\
你可以像这样读取、更改这些配置值：
::

    app.debug = True

一次更新多个配置值，你可以使用 :meth:`dict.update` 方法：
::

    app.config.update(
        DEBUG=True,
        SECRET_KEY='...'
    )

内置配置参数
-----------------

以下配置参数是Flask中默认包含的：

.. tabularcolumns:: |p{6.5cm}|p{8.5cm}|

================================= ==========================================
``DEBUG``                         开启/关闭 debug 模式
``TESTING``                       开启/关闭 测试模式
``PROPAGATE_EXCEPTIONS``          开启/关闭 异常通知
 
                                  当测试或DEBUG模式开启时，\
                                  不管这个值没有设定或者设定为 `None` \
                                  ，程序都会按这个值为 `True` 的情况执行。
``PRESERVE_CONTEXT_ON_EXCEPTION`` 默认情况下，在debug模式中关于异常的详细\
                                  请求信息不会被显示用以方便查看细节数据。\
                                  您可以利用这个配置键打开这个功能。\
                                  您也可以强制使用这个配置开启在非debug\
                                  模式中，这对用于生产环境的应用会很有\
                                  帮助，但是也存在着非常大的风险。
``SECRET_KEY``                    配置程序密钥
``SESSION_COOKIE_NAME``           配置Session Cookie的变量名
``PERMANENT_SESSION_LIFETIME``    配置常驻session对象\
                                  （ :class:`datetime.timedelta` ）\
                                  的保存时长。
``USE_X_SENDFILE``                开启/关闭 x-sendfile
``LOGGER_NAME``                   配置logger的名字
``SERVER_NAME``                   配置服务器的名字和端口号。\
                                  用于对于子域名的支持。\
                                  （例子： ``'localhost:5000'`` ）
``MAX_CONTENT_LENGTH``            配置最大请求内容长度。\
                                  如果提交的内容的字节长度大于此值\
                                  Flask将会拒绝请求，并且返回413状态码。
================================= ==========================================

.. admonition:: 关于 ``SERVER_NAME``

   ``SERVER_NAME`` 值用于对于子域名的支持。\
   因为，在没有获取真实Server Name的情况下，Flask不获取得到子域名。\
   所以当你需要使用子域名的时候需要配置 ``SERVER_NAME`` 。\ 
   这个值也会被session cookie用到。

   Please keep in mind that not only Flask has the problem of not knowing
   what subdomains are, your web browser does as well.  Most modern web
   browsers will not allow cross-subdomain cookies to be set on a
   server name without dots in it.  So if your server name is
   ``'localhost'`` you will not be able to set a cookie for
   ``'localhost'`` and every subdomain of it.  Please chose a different
   server name in that case, like ``'myapplication.local'`` and add
   this name + the subdomains you want to use into your host config
   or setup a local `bind`_.

.. _bind: https://www.isc.org/software/bind

.. versionadded:: 0.4
   ``LOGGER_NAME``

.. versionadded:: 0.5
   ``SERVER_NAME``

.. versionadded:: 0.6
   ``MAX_CONTENT_LENGTH``

.. versionadded:: 0.7
   ``PROPAGATE_EXCEPTIONS``, ``PRESERVE_CONTEXT_ON_EXCEPTION``

使用配置文件
----------------------

Configuration becomes more useful if you can configure from a file, and
ideally that file would be outside of the actual application package so that
you can install the package with distribute (:ref:`distribute-deployment`)
and still modify that file afterwards.

So a common pattern is this::

    app = Flask(__name__)
    app.config.from_object('yourapplication.default_settings')
    app.config.from_envvar('YOURAPPLICATION_SETTINGS')

This first loads the configuration from the
`yourapplication.default_settings` module and then overrides the values
with the contents of the file the :envvar:`YOURAPPLICATION_SETTINGS`
environment variable points to.  This environment variable can be set on
Linux or OS X with the export command in the shell before starting the
server::

    $ export YOURAPPLICATION_SETTINGS=/path/to/settings.cfg
    $ python run-app.py
     * Running on http://127.0.0.1:5000/
     * Restarting with reloader...

On Windows systems use the `set` builtin instead::

    >set YOURAPPLICATION_SETTINGS=\path\to\settings.cfg

The configuration files themselves are actual Python files.  Only values
in uppercase are actually stored in the config object later on.  So make
sure to use uppercase letters for your config keys.

Here is an example configuration file::

    DEBUG = False
    SECRET_KEY = '?\xbf,\xb4\x8d\xa3"<\x9c\xb0@\x0f5\xab,w\xee\x8d$0\x13\x8b83'

Make sure to load the configuration very early on so that extensions have
the ability to access the configuration when starting up.  There are other
methods on the config object as well to load from individual files.  For a
complete reference, read the :class:`~flask.Config` object's
documentation.


最佳配置实践
----------------------------

The downside with the approach mentioned earlier is that it makes testing
a little harder.  There is no one 100% solution for this problem in
general, but there are a couple of things you can do to improve that
experience:

1.  create your application in a function and register blueprints on it.
    That way you can create multiple instances of your application with
    different configurations attached which makes unittesting a lot
    easier.  You can use this to pass in configuration as needed.

2.  Do not write code that needs the configuration at import time.  If you
    limit yourself to request-only accesses to the configuration you can
    reconfigure the object later on as needed.


开发 / 产品
------------------------

Most applications need more than one configuration.  There will at least
be a separate configuration for a production server and one used during
development.  The easiest way to handle this is to use a default
configuration that is always loaded and part of version control, and a
separate configuration that overrides the values as necessary as mentioned
in the example above::

    app = Flask(__name__)
    app.config.from_object('yourapplication.default_settings')
    app.config.from_envvar('YOURAPPLICATION_SETTINGS')

Then you just have to add a separate `config.py` file and export
``YOURAPPLICATION_SETTINGS=/path/to/config.py`` and you are done.  However
there are alternative ways as well.  For example you could use imports or
subclassing.

What is very popular in the Django world is to make the import explicit in
the config file by adding an ``from yourapplication.default_settings
import *`` to the top of the file and then overriding the changes by hand.
You could also inspect an environment variable like
``YOURAPPLICATION_MODE`` and set that to `production`, `development` etc
and import different hardcoded files based on that.

An interesting pattern is also to use classes and inheritance for
configuration::

    class Config(object):
        DEBUG = False
        TESTING = False
        DATABASE_URI = 'sqlite://:memory:'

    class ProductionConfig(Config):
        DATABASE_URI = 'mysql://user@localhost/foo'
    
    class DevelopmentConfig(Config):
        DEBUG = True

    class TestingConfig(Config):
        TESTING = True

开启这个配置你需要调用 :meth:`~flask.Config.from_object` ：
::

    app.config.from_object('configmodule.ProductionConfig')

There are many different ways and it's up to you how you want to manage
your configuration files.  However here a list of good recommendations:

-   keep a default configuration in version control.  Either populate the
    config with this default configuration or import it in your own
    configuration files before overriding values.
-   use an environment variable to switch between the configurations.
    This can be done from outside the Python interpreter and makes
    development and deployment much easier because you can quickly and
    easily switch between different configs without having to touch the
    code at all.  If you are working often on different projects you can
    even create your own script for sourcing that activates a virtualenv
    and exports the development configuration for you.
-   Use a tool like `fabric`_ in production to push code and
    configurations separately to the production server(s).  For some
    details about how to do that, head over to the
    :ref:`fabric-deployment` pattern.

.. _fabric: http://fabfile.org/
