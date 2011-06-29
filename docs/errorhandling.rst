.. _application-errors:

Handling Application Errors 处理应用异常
=====================================
:译者: plucury#gmail.com

.. versionadded:: 0.3

Applications fail, servers fail.  Sooner or later you will see an exception
in production.  Even if your code is 100% correct, you will still see
exceptions from time to time.  Why?  Because everything else involved will
fail.  Here some situations where perfectly fine code can lead to server
errors:

应用程序处理失败，服务器处理失败。在你的产品中这些异常迟早会暴露出来，即使你的代码是完全正确的，
你仍然会一次次的面对这些异常。原因？因为所有的一切都有可能失败。在以下的几种情况中，完美的代码
却导致了服务器的错误：

-   the client terminated the request early and the application was still
    reading from the incoming data.
-   the database server was overloaded and could not handle the query.
-   a filesystem is full
-   a harddrive crashed
-   a backend server overloaded
-   a programming error in a library you are using
-   network connection of the server to another system failed.

-	当应用系统正在读取传入的数据时，客户端过早的结束了请求。
-	数据库超过负荷，无法处理查询请求。
-	文件系统没有空间了。
-	硬盘挂了。
-	终端服务器超过负荷。
-	你所使用的代码库中存在编程错误。
-	服务器与其他系统的网络连接中断了。

And that's just a small sample of issues you could be facing.  So how do we
deal with that sort of problem?  By default if your application runs in
production mode, Flask will display a very simple page for you and log the
exception to the :attr:`~flask.Flask.logger`.

而这只是你所要面对的问题中一些最简单的例子。那我们将如何来解决这些问题呢？在默认的情况下，你的
应用程序在生产模式下运行，Flask将显示一个十分简单的页面并记录这些异常通过使用 :attr:`~flask.Flask.logger`。

But there is more you can do, and we will cover some better setups to deal
with errors.

但是你可以做得更多，并且我们将会讨论几种更好的方案来处理这些异常。

Error Mails 报错邮件
------------------

If the application runs in production mode (which it will do on your
server) you won't see any log messages by default.  Why is that?  Flask
tries to be a zero-configuration framework.  Where should it drop the logs
for you if there is no configuration?  Guessing is not a good idea because
chances are, the place it guessed is not the place where the user has
permission to create a logfile.  Also, for most small applications nobody
will look at the logs anyways.

如果应用程序以生产模式运行（通常在服务器上你会这么做)，在默认情况下你不会看见任何的日志信息。
这是为什么呢？因为Flask是一个零配置框架，而如果没有配置的话，框架又应该把日志文件放到哪里去
呢？依靠假设并不是一个很好的方法，因为总是会存在各种不同的可能，也许那个我们假设放置日志的地方
用户并没有权限访问。另外，对于大多数小型的应用程序来说也不会有人去关注他的日志。

In fact, I promise you right now that if you configure a logfile for the
application errors you will never look at it except for debugging an issue
when a user reported it for you.  What you want instead is a mail the
second the exception happened.  Then you get an alert and you can do
something about it.

实际上，我可以向你保证即使你为你的程序配置了放置错误信息的日志文件，你也永远不会去查看他，除非
当你的用户向你报告了一个事件而你需要去排查错误的时候。你所需要的只是，当异常第二次发生时接收到
一封报警邮件，然后你在针对其中的情况进行处理。

Flask uses the Python builtin logging system, and it can actually send
you mails for errors which is probably what you want.  Here is how you can
configure the Flask logger to send you mails for exceptions:

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

So what just happened?  We created a new
:class:`~logging.handlers.SMTPHandler` that will send mails with the mail
server listening on ``127.0.0.1`` to all the `ADMINS` from the address
*server-error@example.com* with the subject "YourApplication Failed".  If
your mail server requires credentials, these can also be provided.  For
that check out the documentation for the
:class:`~logging.handlers.SMTPHandler`.

这是如何操作的呢？我们创建了一个新的类 :class:`~logging.handlers.SMTPHandler` ，他
将通过  ``127.0.0.1`` 的邮件服务器向所有的 `ADMINS` 用户发送标题为“YourApplication Failed”
邮件，并且将发件地址配置为 *server-error@example.com* 。此外，我们还提供了对
需要证书的邮件服务器的支持，关于这部分的文档，请查看 :class:`~logging.handlers.SMTPHandler` 。

We also tell the handler to only send errors and more critical messages.
Because we certainly don't want to get a mail for warnings or other
useless logs that might happen during request handling.

邮件处理器只会发送异常和错误的信息，因为我们并不希望通过邮件获取警告信息或其他一些处理过程中
产生的没有用的日志。


Before you run that in production, please also look at :ref:`logformat` to
put more information into that error mail.  That will save you from a lot
of frustration.

当你在产品中使用它们的时候，请务必查看 :ref:`logformat` 以使得报错邮件中包含更多的信息。这
些信息将为你解决很多的烦恼。

Logging to a File 日志文件
-------------------------

Even if you get mails, you probably also want to log warnings.  It's a
good idea to keep as much information around that might be required to
debug a problem.  Please note that Flask itself will not issue any
warnings in the core system, so it's your responsibility to warn in the
code if something seems odd.

即使你已经有了报错邮件，你可能仍然希望能够查看到警告信息。为了排查问题，尽可能的保存更多的
信息不失为一个好主意。请注意，Flask的系统核心本身并不会去记录任何警告信息，因此编写记录那
些看起来不对劲的地方的代码将是你的责任。

There are a couple of handlers provided by the logging system out of the
box but not all of them are useful for basic error logging.  The most
interesting are probably the following:

这里提供了几个处理类，但对于基本的记录错误日志而言他们并不是总是那么的有用。而其中最值得我们
注意的是以下几项:

-   :class:`~logging.handlers.FileHandler` - logs messages to a file on the
    filesystem.
    
-	:class:`~logging.handlers.FileHandler` - 将日志信息写入文件系统中

-   :class:`~logging.handlers.RotatingFileHandler` - logs messages to a file
    on the filesystem and will rotate after a certain number of messages.

-   :class:`~logging.handlers.RotatingFileHandler` - 将日志信息写入文件系统中，并且
	当日志达到一定数量时会滚动记录最新的信息。

-   :class:`~logging.handlers.NTEventLogHandler` - will log to the system
    event log of a Windows system.  If you are deploying on a Windows box,
    this is what you want to use.
    
-   :class:`~logging.handlers.NTEventLogHandler` - 将日志发送到windows系统的日
	志事件中。如果你的系统部署在windows环境中，那么这正是你想要的。
    
-   :class:`~logging.handlers.SysLogHandler` - sends logs to a UNIX
    syslog.

-   :class:`~logging.handlers.SysLogHandler` - 将日志发送到UNIX的系统日志中。

Once you picked your log handler, do like you did with the SMTP handler
above, just make sure to use a lower setting (I would recommend
`WARNING`):

一旦你选择了你的日志处理类，你就可以向上文中配置SMTP处理类一样的来配置它们，唯一需要注意的
是使用更低级别的设置（我这里使用的是`WARNING`）::

    if not app.debug:
        import logging
        from logging.handlers import TheHandlerYouWant
        file_handler = TheHandlerYouWant(...)
        file_handler.setLevel(logging.WARNING)
        app.logger.addHandler(file_handler)

.. _logformat:

Controlling the Log Format
--------------------------

By default a handler will only write the message string into a file or
send you that message as mail.  A log record stores more information,
and it makes a lot of sense to configure your logger to also contain that
information so that you have a better idea of why that error happened, and
more importantly, where it did.

A formatter can be instantiated with a format string.  Note that
tracebacks are appended to the log entry automatically.  You don't have to
do that in the log formatter format string.

Here some example setups:

Email
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

File logging
````````````

::

    from logging import Formatter
    file_handler.setFormatter(Formatter(
        '%(asctime)s %(levelname)s: %(message)s '
        '[in %(pathname)s:%(lineno)d]'
    ))


Complex Log Formatting
``````````````````````

Here is a list of useful formatting variables for the format string.  Note
that this list is not complete, consult the official documentation of the
:mod:`logging` package for a full list.

.. tabularcolumns:: |p{3cm}|p{12cm}|

+------------------+----------------------------------------------------+
| Format           | Description                                        |
+==================+====================================================+
| ``%(levelname)s``| Text logging level for the message                 |
|                  | (``'DEBUG'``, ``'INFO'``, ``'WARNING'``,           |
|                  | ``'ERROR'``, ``'CRITICAL'``).                      |
+------------------+----------------------------------------------------+
| ``%(pathname)s`` | Full pathname of the source file where the         |
|                  | logging call was issued (if available).            |
+------------------+----------------------------------------------------+
| ``%(filename)s`` | Filename portion of pathname.                      |
+------------------+----------------------------------------------------+
| ``%(module)s``   | Module (name portion of filename).                 |
+------------------+----------------------------------------------------+
| ``%(funcName)s`` | Name of function containing the logging call.      |
+------------------+----------------------------------------------------+
| ``%(lineno)d``   | Source line number where the logging call was      |
|                  | issued (if available).                             |
+------------------+----------------------------------------------------+
| ``%(asctime)s``  | Human-readable time when the LogRecord` was        |
|                  | created.  By default this is of the form           |
|                  | ``"2003-07-08 16:49:45,896"`` (the numbers after   |
|                  | the comma are millisecond portion of the time).    |
|                  | This can be changed by subclassing the formatter   |
|                  | and overriding the                                 |
|                  | :meth:`~logging.Formatter.formatTime` method.      |
+------------------+----------------------------------------------------+
| ``%(message)s``  | The logged message, computed as ``msg % args``     |
+------------------+----------------------------------------------------+

If you want to further customize the formatting, you can subclass the
formatter.  The formatter has three interesting methods:

:meth:`~logging.Formatter.format`:
    handles the actual formatting.  It is passed a
    :class:`~logging.LogRecord` object and has to return the formatted
    string.
:meth:`~logging.Formatter.formatTime`:
    called for `asctime` formatting.  If you want a different time format
    you can override this method.
:meth:`~logging.Formatter.formatException`
    called for exception formatting.  It is passed an :attr:`~sys.exc_info`
    tuple and has to return a string.  The default is usually fine, you
    don't have to override it.

For more information, head over to the official documentation.


Other Libraries
---------------

So far we only configured the logger your application created itself.
Other libraries might log themselves as well.  For example, SQLAlchemy uses
logging heavily in its core.  While there is a method to configure all
loggers at once in the :mod:`logging` package, I would not recommend using
it.  There might be a situation in which you want to have multiple
separate applications running side by side in the same Python interpreter
and then it becomes impossible to have different logging setups for those.

Instead, I would recommend figuring out which loggers you are interested
in, getting the loggers with the :func:`~logging.getLogger` function and
iterating over them to attach handlers::

    from logging import getLogger
    loggers = [app.logger, getLogger('sqlalchemy'),
               getLogger('otherlibrary')]
    for logger in loggers:
        logger.addHandler(mail_handler)
        logger.addHandler(file_handler)
