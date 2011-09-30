.. _installation:

安装
============
:译者: suxindichen@douban

Flask依靠两个外部库， `Werkzeug <http://werkzeug.pocoo.org/>`_ 和 
`Jinja2 <http://jinja.pocoo.org/2/>`_. Werkzeug是一个WSGI的工具包，
在web应用和多种服务器之间开发和部署的标准的python 接口。Jinja2呈现模板。 

那么如何快速获得你计算机中的一切？在这个章节中会介绍很多种方式，但是最了
不起的要数virtualenv,所以我们第一个先说它。 

.. _virtualenv:

virtualenv
----------

当你拥有shell访问权限时，virtualenv 可能是你在开发以及生产环境中想要使用的。 

Virtualenv解决了什么问题？如果你像我一样喜欢Python，你可能会不仅想要在基于
Flask的Web应用，还包括一些其他的应用中使用它。但是，你拥有的项目越多，你用
不同的版本的Python工作的可能性越大，或者至少是不同版本的Python库。面对现实
吧；库很经常的破坏向后兼容性，而且想要任何大型的（正经的）应用零依赖是不可
能的。那么当你的两个或多个项目有依赖性冲突的话，你要怎么做？

Virtualenv来救援！它从根本上实现了多种并排式的python安装。它实际上并没有安
装Python的单独的副本，但它确实提供了一种巧妙的方式，让不同的项目环境中分离
出来。 

那么让我们来看看Virtualenv是如何工作的！ 

如果你是在Mac OS X 或者Linux下，那么下面的两条命令将会适合你::

    $ sudo easy_install virtualenv

或者更好的::

    $ sudo pip install virtualenv


任意一个都可以在你的系统中安装virtualenv。它甚至可能在你的包管理中。如果你使用
的是Ubuntu，尝试::

    $ sudo apt-get install python-virtualenv

如果你在Windows平台上并没有 `easy_install` 命令，你首先必须安装它。查阅 
:ref:`windows-easy-install` 章节来获得更多如何做的信息。一旦你安装了它，
运行上述的命令，记得去掉 `sudo` 前缀。 

一旦你装上了virtualenv，请调出shell然后创建你自己的环境变量。我通常会创建
一个包含 `env` 文件夹的项目文件夹：
::

    $ mkdir myproject
    $ cd myproject
    $ virtualenv env
    New python executable in env/bin/python
    Installing setuptools............done.


现在，无论何时你想在一个项目上工作，你只需要激活相应的环境。在OS X和Linux上
，执行以下操作：
::

    $ . env/bin/activate

(注意脚本名称和点号之间的空格。该点意味着这个脚本应该运行在当前shell的上下文。
如果这条命令不能在你的shell中正常工作，请试着把点号替换为 ``source``)

如果你是一个Windows用户，下面的命令是为你准备的::

    $ env\scripts\activate

无论哪种方式，现在你应该正在使用你的virtualenv（看看你的shell提示已经更改到
显示virtualenv） 

现在你可以键入下面的命令来激活你virtualenv中的Flask::

    $ easy_install Flask

几秒钟后就准备好了。 

安装到系统全局
------------------------

这样也可以，但是我确实不推荐它。只需以root权限运行 `easy_install` 
:: 

    $ sudo easy_install Flask

(Windows平台下，在管理员Shell下运行,不要 `sudo` ).


生活在边缘 
------------------

如果你想要使用最新版本的Flask，有两种方法：你可以使用 `easy_insall` 拉出开发版本，
或者让它来操作一个git检索。无论哪种方式，推荐你使用virtualenv。 

在一个新的Virtualenv中获得git检索,并运行在在开发模式下 ::

    $ git clone http://github.com/mitsuhiko/flask.git
    Initialized empty Git repository in ~/dev/flask/.git/
    $ cd flask
    $ virtualenv env
    $ . env/bin/activate
    New python executable in env/bin/python
    Installing setuptools............done.
    $ python setup.py develop
    ...
    Finished processing dependencies for Flask

这将引入依赖关系和激活Git的头作为在Virtualenv中当前的版本。然后你只需
要 ``git pull origin`` 来获得最新的版本。 

如果你不想用git来得到最新的开发版，可以改用下面的命令::

    $ mkdir flask
    $ cd flask
    $ virtualenv env
    $ . env/bin/activate
    New python executable in env/bin/python
    Installing setuptools............done.
    $ easy_install Flask==dev
    ...
    Finished processing dependencies for Flask==dev

.. _windows-easy-install:

Windows 平台下的 `easy_install`
---------------------------------

在windows上，安装 `easy_install` 是有一点的复杂因为在Windows上比在类Unix系统上
有一些轻微的不同的规则，但是它并不难。最简单的安装方式是下载 `ez_setup.py`_ 文件
然后运行它。运行它最简单的方式是进入到你的下载目录中，然后双击这个文件。 

接着，添加 `easy_install` 命令和其他Python脚本到命令行搜索路径，方法为：添加你
python安装目录中的Scripts文件夹到环境变量 `PATH` 中。添加方法:右键桌面的“我的电脑”
图标或者开始菜单中的“计算机”，然后选在“属性”。之后，在Vista和Win7下，单击“高级系统
设置”；在WinXP下，单击“高级”选项。然后，单击“环境变量”按钮，双击“系统变量”中的“path”变量。
在那里添加你的Python解释器的 Scripts文件夹；确保你使用分号将它与现有的值隔开。 
假设你在使用默认路径的Python2.6，加入下面的值 ::

    ;C:\Python26\Scripts

这样就完成了。要检查它是否正常工作，打开命令提示符然后执行 ``easy_install``.如果在Vista
或者Win7下你只有用户控制权限，它应该会要求你获得管理员权限。 

.. _ez_setup.py: http://peak.telecommunity.com/dist/ez_setup.py
