Flask中的Unicode
=================

Flask就像Jinja2和Werkzeug那样，是完全基于Unicode的。
不只是这几个库，绝大多数的Python中网络相关的库都是这样处理文本的。
如果你对Unicode还不够了解，你可以阅读这篇文章 `The Absolute Minimum Every Software Developer
Absolutely, Positively Must Know About Unicode and Character Sets
<http://www.joelonsoftware.com/articles/Unicode.html>`_ 。
这部分文档只是希望能帮助你了解一些基础知识，这样你就可以处理一些与Unicode有关的东西了。

自动转换
--------------------

Flask默认基于以下一些假设（当然，你可以更改），给予你一些基础的、简单的Unicode支持：

-   你的网站的源代码使用的是UTF-8编码。
-   在程序内部你将始终使用Unicode，除非对于只有ASCII编码的字符的字符串。
-   编码、解码只会发生在你需要用某种协议传输字节（bytes）形式的数据。    

这对于你有什么用呢？

HTTP协议基于字节码（bytes）。
不仅是协议，
也用于标记文件在服务器位置（即URI、URL）的系统中。

However HTML which
is usually transmitted on top of HTTP supports a large variety of
character sets and which ones are used, are transmitted in an HTTP header.
To not make this too complex Flask just assumes that if you are sending
Unicode out you want it to be UTF-8 encoded.  Flask will do the encoding
and setting of the appropriate headers for you.

The same is true if you are talking to databases with the help of
SQLAlchemy or a similar ORM system.  Some databases have a protocol that
already transmits Unicode and if they do not, SQLAlchemy or your other ORM
should take care of that.

The Golden Rule
---------------

So the rule of thumb: if you are not dealing with binary data, work with
Unicode.  What does working with Unicode in Python 2.x mean?

-   as long as you are using ASCII charpoints only (basically numbers,
    some special characters of latin letters without umlauts or anything
    fancy) you can use regular string literals (``'Hello World'``).
-   if you need anything else than ASCII in a string you have to mark
    this string as Unicode string by prefixing it with a lowercase `u`.
    (like ``u'Hänsel und Gretel'``)
-   if you are using non-Unicode characters in your Python files you have
    to tell Python which encoding your file uses.  Again, I recommend
    UTF-8 for this purpose.  To tell the interpreter your encoding you can
    put the ``# -*- coding: utf-8 -*-`` into the first or second line of
    your Python source file.
-   Jinja is configured to decode the template files from UTF-8.  So make
    sure to tell your editor to save the file as UTF-8 there as well.

Encoding and Decoding Yourself
------------------------------

If you are talking with a filesystem or something that is not really based
on Unicode you will have to ensure that you decode properly when working
with Unicode interface.  So for example if you want to load a file on the
filesystem and embed it into a Jinja2 template you will have to decode it
from the encoding of that file.  Here the old problem that text files do
not specify their encoding comes into play.  So do yourself a favour and
limit yourself to UTF-8 for text files as well.

Anyways.  To load such a file with Unicode you can use the built-in
:meth:`str.decode` method::

    def read_file(filename, charset='utf-8'):
        with open(filename, 'r') as f:
            return f.read().decode(charset)

To go from Unicode into a specific charset such as UTF-8 you can use the
:meth:`unicode.encode` method::

    def write_file(filename, contents, charset='utf-8'):
        with open(filename, 'w') as f:
            f.write(contents.encode(charset))

Configuring Editors
-------------------

Most editors save as UTF-8 by default nowadays but in case your editor is
not configured to do this you have to change it.  Here some common ways to
set your editor to store as UTF-8:

-   Vim: put ``set enc=utf-8`` to your ``.vimrc`` file.

-   Emacs: either use an encoding cookie or put this into your ``.emacs``
    file::

        (prefer-coding-system 'utf-8)
        (setq default-buffer-file-coding-system 'utf-8)

-   Notepad++:

    1. Go to *Settings -> Preferences ...*
    2. Select the "New Document/Default Directory" tab
    3. Select "UTF-8 without BOM" as encoding

    It is also recommended to use the Unix newline format, you can select
    it in the same panel but this is not a requirement.
