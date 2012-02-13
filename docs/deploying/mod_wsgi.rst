.. _mod_wsgi-deployment:

mod_wsgi (Apache)
=================

如果你使用 `Apache`_ 作为Web服务器, 你可以考虑使用 `mod_wsgi`_.

.. admonition:: 注意

   请事先确认你应用程序内的所有 ``app.run()`` 调用包含在 ``if __name__ ==  '__main__':`` 区块内或在一个单独的文件里。 要确认这个的原因是因为这句语句执行后总是会启动一个新的本地WSGI服务器，但在部署到mod_wsgi的环境中，我们不需要它。 

.. _Apache: http://httpd.apache.org/

安装 `mod_wsgi`
---------------------

如果你还没有安装 `mod_wsgi` ，你需要自己去下载安装或者自行编译。你可以点击 `安装指南`_ 来学习如何在UNIX系统下安装mod_wsgi。

如果你使用Ubuntu或Debian，你可以使用apt-get来启用它，如下所示：

.. sourcecode:: text

    # apt-get install libapache2-mod-wsgi

在FreeBSD上安装`mod_wsgi`可以通过编译 `www/mod_wsgi` 端口或者使用pkg_add:

.. sourcecode:: text

    # pkg_add -r mod_wsgi

如果你使用pkgsrc，你可以通过编译 `www/ap2-wsgi` 包来安装 `mod_wsgi` 。

如果在第一次apache重启后出现segfaulting child processes（子进程段错误），你可以直接的无视。再重启一下即可。

创建一个 `.wsgi` 文件
-----------------------

要运行你的应用程序，你需要一个 `yourapplication.wsgi` 文件。这个文件包含 `mod_wsgi` 在启动时需要执行的获取应用程序对象的代码。该对象在那个文件里调用了 `application` 然后就会把它当作应用程序来处理了。

对于大多数应用程序而言，用下面这样的一个文件就足够了::

    from yourapplication import app as application

如果你没有创建应用程序对象的工厂方法，只有一个单独的实例，你可以直接将其作为 `application` 直接import（导入）。

找一个地方把这个文件放好，以便于你可以再次找到它 (举例:`/var/www/yourapplication`) 并且确认 `yourapplication` 以及所有你已经使用到的类库在python可以读取的路径内。如果你不希望整个系统使用同一个运行环境，你可以考虑创建一个 `虚拟 python`_ 环境。

配置 Apache
------------------

你要做的最后一件事就是为你的应用程序建立一个Apache配置文件。基于安全方面的原因，在这个实例里我们会让 `mod_wsgi` 在不同的用户环境下执行应用程序：

.. sourcecode:: apache

    <VirtualHost *>
        ServerName example.com

        WSGIDaemonProcess yourapplication user=user1 group=group1 threads=5
        WSGIScriptAlias / /var/www/yourapplication/yourapplication.wsgi

        <Directory /var/www/yourapplication>
            WSGIProcessGroup yourapplication
            WSGIApplicationGroup %{GLOBAL}
            Order deny,allow
            Allow from all
        </Directory>
    </VirtualHost>

如需要更多信息请参考 `mod_wsgi 维基`_.

.. _mod_wsgi: http://code.google.com/p/modwsgi/
.. _安装指南: http://code.google.com/p/modwsgi/wiki/QuickInstallationGuide
.. _虚拟 python: http://pypi.python.org/pypi/virtualenv
.. _mod_wsgi 维基: http://code.google.com/p/modwsgi/wiki/

常见问题
---------------

如果你的应用程序没有运行，请跟着以下步骤来排错:

**问题:** 应用程序没有运行，错误日志显示SystemExit ignored
    在你的应用程序文件里有某处调用了 ``app.run()`` ，但是没有包含在 ``if __name__ == '__main__':`` 条件内。你可以将这个文件里的调用方法移到一个单独的 `run.py` 文件或者给它加上一个if语块。

**问题:** 应用程序抛出permission（许可）错误
    这个可能是由于运行你的应用程序的用户不正确。请确认应用程序所在目录的用户访问权限使应用程序获得所需的执行条件，且再次确认实际用户与配置用户是否一致。(确认 `WSGIDaemonProcess` 命令的 ``用户`` 和 ``组`` 参数)

**问题:** 应用程序挂了并且输出了错误信息
    请记住 mod_wsgi 不允许做任何的 :data:`sys.stdout` 和 :data:`sys.stderr` 操作。你可以配置文件里设置 `WSGIRestrictStdout` 的值为 ``off`` 来禁用该保护：

    .. sourcecode:: apache

        WSGIRestrictStdout Off

    或者你也可以在.wsgi文件里用一个不一样的流替换标准输出::

        import sys
        sys.stdout = sys.stderr

**问题:** 访问资源时出现IO错误
    你的应用程序可能是一个单独的.py文件通过快捷方式（符号链接）指向site-packages目录。要知道这样是不行的，要修复这个错误你必须将此目录放到这个文件实际所在的python路径，或者将你的应用程序转成一个包。

    这么做的理由是对于没有安装过的包来说，filename模块用户定位资源，而对于快捷方式（符号链接）来说就等于调用了错误的filename模块。

自动重载的支持
-------------------------------

为了部署更加方便，你可以启用自动重载功能。就是说在 `.wsgi` 文件内有任意变更， `mod_wsgi` 就会为我们重载所有的后台进程。

关于这个的实现，只需要在你的 `Directory` 配置块内加入以下指令即可:

.. sourcecode:: apache

   WSGIScriptReloading On

在虚拟环境下工作
---------------------------------

虚拟环境有很明显的优点。比如你无需在整个系统环境下配置所有的依赖且只能用同一个版本，虚拟环境可以在任何地方随心所欲的作环境的版本控制。不过如果你需要在mod_wsgi配合下使用虚拟环境，你必须对 `.wsgi` 作些许的修改。

在你的 `.wsgi` 文件的顶部插入如下行::

    activate_this = '/path/to/env/bin/activate_this.py'
    execfile(activate_this, dict(__file__=activate_this))

这两句话根据设置的虚拟环境建立了要载入的路径。要谨记这里必须要用绝对地址。
