
KaniMySQL
=========

This is the fork from DictMySQL and change it to use AttrDict and use like ORM.

Concept
-------

While developping with ORM such as SQLAlchemy, ORM object management can execute unexpected queries. Especially after commit execution, all the objects need to execute SELECT query in the case of changing values. It is not a few times unnecessary. So KaniMySQL does require select queries when accessing a modified object. And update method is needed to apply changes to the DB.

How to use
----------

All table must have autoincrement column named ``id`` like SQLAlchemy. 

Anything else, just see the ``example.py``. ``where`` method is mostly same as ``DictMySQL``.
