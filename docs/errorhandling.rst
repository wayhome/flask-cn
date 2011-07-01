.. _application-errors:

处理应用异常
==========
:译者: plucury#gmail.com

.. versionadded:: 0.3

应用程序处理失败，服务器处理失败。在你的产品中这些异常迟早会暴露出来，即使你的代码是完全正确的，
你仍然会一次次的面对这些异常。原因？因为所有的一切都有可能失败。在以下的几种情况中，完美的代码
却导致了服务器的错误：

-	当应用系统正在读取传入的数据时，客户端过早的结束了请求。
-	数据库超过负荷，无法处理查询请求。
-	文件系统没有空间了。
-	硬盘挂了。
-	终端服务器超过负荷。
-	你所使用的代码库中存在编程错误。
-	服务器与其他系统的网络连接中断了。

而这只是你所要面对的问题中一些最简单的例子。那我们将如何来解决这些问题呢？在默认的情况下，你的
应用程序在生产模式下运行，Flask将显示一个十分简单的页面并记录这些异常通过使用 :attr:`~flask.Flask.logger`。

但是你可以做得更多，并且我们将会讨论几种更好的方案来处理这些异常。

报错邮件
------
如果应用程序以生产模式运行（通常在服务器上你会这么做)，在默认情况下你不会看见任何的日志信息。
这是为什么呢？因为Flask是一个零配置框架，而如果没有配置的话，框架又应该把日志文件放到哪里去
呢？依靠假设并不是一个很好的方法，因为总是会存在各种不同的可能，也许那个我们假设放置日志的地方
用户并没有权限访问。另外，对于大多数小型的应用程序来说也不会有人去关注他的日志。

实际上，我可以向你保证即使你为你的程序配置了放置错误信息的日志文件，你也永远不会去查看他，除非
当你的用户向你报告了一个事件而你需要去排查错误的时候。你所需要的只是，当异常第二次发生时接收到
一封报警邮件，然后你在针对其中的情况进行处理。

Flask使用了python内置的日志系统，并且他会在你需要是向你发生关于异常的邮件。这里是一个关于如何
配置Flask的日志以向你发送异常邮件的例子::


    ADMINS = ['yourname@example.com']
    if not app.debug:
        import logging
        from logging.handlers import SMTPHandler
        mail_handler = SMTPHandler('127.0.0.1',
                                   'server-error@example.com',
                                   ADMINS, 'YourApplication Failed')
        mail_handler.setLevel(logging.ERROR)
        app.logger.addHandler(mail_handler)

这是如何操作的呢？我们创建了一个新的类 :class:`~logging.handlers.SMTPHandler` ，他
将通过  ``127.0.0.1`` 的邮件服务器向所有的 `ADMINS` 用户发送标题为“YourApplication Failed”
邮件，并且将发件地址配置为 *server-error@example.com* 。此外，我们还提供了对
需要证书的邮件服务器的支持，关于这部分的文档，请查看 :class:`~logging.handlers.SMTPHandler` 。

邮件处理器只会发送异常和错误的信息，因为我们并不希望通过邮件获取警告信息或其他一些处理过程中
产生的没有用的日志。

当你在产品中使用它们的时候，请务必查看 :ref:`logformat` 以使得报错邮件中包含更多的信息。这
些信息将为你解决很多的烦恼。

日志文件
------
即使你已经有了报错邮件，你可能仍然希望能够查看到警告信息。为了排查问题，尽可能的保存更多的
信息不失为一个好主意。请注意，Flask的系统核心本身并不会去记录任何警告信息，因此编写记录那
些看起来不对劲的地方的代码将是你的责任。

这里提供了几个处理类，但对于基本的记录错误日志而言他们并不是总是那么的有用。而其中最值得我们
注意的是以下几项:

-	:class:`~logging.handlers.FileHandler` - 将日志信息写入文件系统中

-   :class:`~logging.handlers.RotatingFileHandler` - 将日志信息写入文件系统中，并且
当日志达到一定数量时会滚动记录最新的信息。
    
-   :class:`~logging.handlers.NTEventLogHandler` - 将日志发送到windows系统的日
志事件中。如果你的系统部署在windows环境中，那么这正是你想要的。

-   :class:`~logging.handlers.SysLogHandler` - 将日志发送到UNIX的系统日志中。

一旦你选择了你的日志处理类，你就可以向上文中配置SMTP处理类一样的来配置它们，唯一需要注意的
是使用更低级别的设置（我这里使用的是 `WARNING`）::

    if not app.debug:
        import logging
        from logging.handlers import TheHandlerYouWant
        file_handler = TheHandlerYouWant(...)
        file_handler.setLevel(logging.WARNING)
        app.logger.addHandler(file_handler)

.. _logformat:

日志格式
------
在默认情况下，处理器只会将日志信息写入文件或是用邮件发送给你。而日志应该记录更多的信息，你必须
配置你的日志，使它能够让你更方便的知道发生了什么样的错误，以及更重要的是告诉你哪里发生了错误。

格式处理器（formatter）可以让你获取格式化的字符串。你需要知道是日志的连接是自动进行的，你不需要
将它包含在格式处理器的格式化字符串中。

这里有几个例子：

电子邮件
`````

::

    from logging import Formatter
    mail_handler.setFormatter(Formatter('''
    Message type:       %(levelname)s
    Location:           %(pathname)s:%(lineno)d
    Module:             %(module)s
    Function:           %(funcName)s
    Time:               %(asctime)s

    Message:

    %(message)s
    '''))

日志文件
``````

::

    from logging import Formatter
    file_handler.setFormatter(Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
        '[in %(pathname)s:%(lineno)d]'
    ))

复杂的日志格式
```````````

这里是一系列用户格式化字符串的变量。这里的列表并不完整，你可以通过查看官方文档的 :mod:`logging` 
部分来获取完整的列表。

.. tabularcolumns:: |p{3cm}|p{12cm}|

+------------------+----------------------------------------------------+
|格式               |描述                                                 |
+==================+====================================================+
| ``%(levelname)s``| 日志等级。                                           |
|                  | (``'DEBUG'``, ``'INFO'``, ``'WARNING'``,           |
|                  | ``'ERROR'``, ``'CRITICAL'``).                      |
+------------------+----------------------------------------------------+
| ``%(pathname)s`` | 调用日志的源文件的全路径（如果可以获得的话）。               |
+------------------+----------------------------------------------------+
| ``%(filename)s`` | 文件名。                                             |
+------------------+----------------------------------------------------+
| ``%(module)s``   | 模块名。                                             |
+------------------+----------------------------------------------------+
| ``%(funcName)s`` | 方法名。                                             |
+------------------+----------------------------------------------------+
| ``%(lineno)d``   | 调用日志的代码所在源文件中的行号。                        |
+------------------+----------------------------------------------------+
| ``%(asctime)s``  | 日志中创建的可读时间。默认的格式是                        |
|                  | ``"2003-07-08 16:49:45,896"`` （逗号后的时间是毫秒）。  |
|                  |可以通过复写 :meth:`~logging.Formatter.formatTime` 方法|
|                  |来修改它。                                            |
+------------------+----------------------------------------------------+
| ``%(message)s``  |日志信息。同 ``msg % args``                           |
+------------------+----------------------------------------------------+

如果你需要更多的定制化格式，你可以实现格式处理器（formatter）的子类。它有以下三个有趣的方法:

:meth:`~logging.Formatter.format`:
    处理实际的格式。它需要接收一个 :class:`~logging.LogRecord` 对象，并返回一个被
    格式话的字符串。
:meth:`~logging.Formatter.formatTime`:
    调用  `asctime` 进行格式化。如果你需要不同的时间格式，可以复写这个方法。
:meth:`~logging.Formatter.formatException`
    调用异常格式化。它接收一个 :attr:`~sys.exc_info` 元组并返回一个字符串。通常它会很好
    的运行，你并不需要复写它。

获取更多的信息，请查看官方文档。


其他代码库
--------
目前为止，我们只配置了你的程序自身的日志。而其他的代码库同样可以需要记录日志。比如，SQLAlchemy
使用了很多日志。使用 :mod:`logging` 包可以一次性的配置所有的日志，当我并不推荐那样做。因为当
多个程序在同一个Python解释器上运行是，你将无法单独的对他们进行配置。

相对的，我推荐你只对你所关注的日志进行配置，通过 :func:`~logging.getLogger` 方法获取
所有的日志处理器，并通过迭代获取他们::

    from logging import getLogger
    loggers = [app.logger, getLogger('sqlalchemy'),
               getLogger('otherlibrary')]
    for logger in loggers:
        logger.addHandler(mail_handler)
        logger.addHandler(file_handler)
