============
Installation
============

Install the package with pip:

.. code:: console

   $ pip install limits

.. tabbed:: Redis

   .. code:: console

      $ pip install limits[redis]

   Includes

   .. literalinclude:: ../../requirements/storage/redis.txt

.. tabbed:: RedisCluster

   .. code:: console

      $ pip install limits[rediscluster]

   Includes

   .. literalinclude:: ../../requirements/storage/rediscluster.txt

.. tabbed:: Memcached

   .. code:: console

      $ pip install limits[memcached]

   Includes

   .. literalinclude:: ../../requirements/storage/memcached.txt

.. tabbed:: MongoDB

   .. code:: console

      $ pip install limits[mongodb]

   Includes:

   .. literalinclude:: ../../requirements/storage/mongodb.txt

More details around the specifics of each storage backend can be
found in :ref:`storage`


Async Storage
=============

If you are using an async code base you can install the storage dependencies
along with the package using the following extras:


.. tabbed:: Redis

   .. code:: console

      $ pip install limits[async-redis]

   Includes:

   .. literalinclude:: ../../requirements/storage/async-redis.txt

.. tabbed:: Memcached

   .. code:: console

      $ pip install limits[async-memcached]

   Includes:

   .. literalinclude:: ../../requirements/storage/async-memcached.txt

.. tabbed:: MongoDB

   .. code:: console

      $ pip install limits[async-mongodb]

   Includes:

   .. literalinclude:: ../../requirements/storage/async-mongodb.txt
