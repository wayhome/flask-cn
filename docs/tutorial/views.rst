.. _tutorial-views:

第五步: 视图函数
================

现在数据库连接已经可以工作了，我们终于可以开始写我们的视图函数了。我们一共
需要写4个：

显示文章
--------

这个视图将会显示数据库中所有的文章。它会绑定在应用的根地址，并且从数据库中
查询出文章的标题和内容。最新发表的文章会显示在最上方。从cursor返回的数据是
存放在一个tuple中，而且以select语句中的指定的顺序排序。对我们这个小应用来说
tuple已经满足要求了，但是也许你想把它转换成dict。那么，你可以参考 
:ref:`easy-querying` 的示例。

视图函数会把所有的文章以字典的方式传送给 `show_entries.html`
模版，然后向浏览器返回render过的::

    @app.route('/')
    def show_entries():
        cur = g.db.execute('select title, text from entries order by id desc')
        entries = [dict(title=row[0], text=row[1]) for row in cur.fetchall()]
        return render_template('show_entries.html', entries=entries)

添加一篇新文章
--------------

这个视图用来让已登陆的用户发表新文章。它只对以 `POST`
方式提交的请求回应，实际的表单显示在 `show_entries`
页面上。如果一切都没有出问题的话，我们用 `~flask.flash`
向下一次请求发送一条信息，然后重定向回 `show_entries` 页面::

    @app.route('/add', methods=['POST'])
    def add_entry():
        if not session.get('logged_in'):
            abort(401)
        g.db.execute('insert into entries (title, text) values (?, ?)',
                     [request.form['title'], request.form['text']])
        g.db.commit()
        flash('New entry was successfully posted')
        return redirect(url_for('show_entries'))

注意，我们在这里检查了用户是否已经登陆（ `logged_in`
键在session中存在，而且值为 `True` ）。

.. admonition:: Security Note

   Be sure to use question marks when building SQL statements, as done in the
   example above.  Otherwise, your app will be vulnerable to SQL injection when
   you use string formatting to build SQL statements.
   See :ref:`sqlite3` for more.

登陆和登出
----------

这些函数是用来让用户登陆和注销的。登陆函数会检查用户名和秘密，并和配置文件
中的数据进行比较，并相应的设置session中的 `logged_in`
键。如果用户登陆成功，那么这个键会被设置成 `True` ，然后用户会被重定向到
`show_entries` 页面。并且还会flash一条消息来提示用户登陆成功。如果登陆发生
错误,那么模版会得知这一点，然后提示用户重新登陆::

    @app.route('/login', methods=['GET', 'POST'])
    def login():
        error = None
        if request.method == 'POST':
            if request.form['username'] != app.config['USERNAME']:
                error = 'Invalid username'
            elif request.form['password'] != app.config['PASSWORD']:
                error = 'Invalid password'
            else:
                session['logged_in'] = True
                flash('You were logged in')
                return redirect(url_for('show_entries'))
        return render_template('login.html', error=error)

注销函数所作的正好相反。它从session中删除 `logged_in` 键。我们在这里使用的
一个简洁的小技巧：如果你在使用字典的 :meth:`~dict.pop` 方法时，给了它第二个
参数（默认），那么这个方法在处理的时候，会先查询是否存在这个键，如果存在，
则删除它，如果不存在，那么什么都不做。这个特性很有用，因为这样我们在处理的
时候，就不需要先检查用户是否已登陆。

::

    @app.route('/logout')
    def logout():
        session.pop('logged_in', None)
        flash('You were logged out')
        return redirect(url_for('show_entries'))

继续 :ref:`tutorial-templates`.
