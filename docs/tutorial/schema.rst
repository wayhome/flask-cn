.. _tutorial-schema:

第一步: 数据库模式
==================

首先我们要创建数据库模式。对于这个应用一个表就足够了，而且我们只需要支持
SQLite，所以很简单。只要把下面的内容放入一个叫 `schema.sql` 的文件中，这
个文件应存放在 `flaskr` 文件夹中：

.. sourcecode:: sql

    drop table if exists entries;
    create table entries (
      id integer primary key autoincrement,
      title string not null,
      text string not null
    );

这个模式由一个叫 `entries` 的表组成，表里面的每一行都有 `id` `title` 
`text` 字段。 `id` 是一个自动增加的整数，而且它是主键，其他的两个是字符
串，而且不能为null

继续 :ref:`tutorial-setup`.
