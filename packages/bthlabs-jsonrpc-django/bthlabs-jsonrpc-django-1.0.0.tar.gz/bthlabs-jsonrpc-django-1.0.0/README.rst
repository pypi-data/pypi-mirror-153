bthlabs-jsonrpc-django
======================

BTHLabs JSONRPC - django integration

`Docs`_ | `Source repository`_

Overview
--------

BTHLabs JSONRPC is a set of Python libraries that provide extensible framework
for adding JSONRPC interfaces to existing Python Web applications.

The *django* package provides Django integration.

Installation
------------

.. code-block:: shell

    $ pip install bthlabs_jsonrpc_django

Example
-------

.. code-block:: python

    # settings.py
    INSTALLED_APPS = [
        # ...
        'bthlabs_jsonrpc_django',
    ]

.. code-block:: python

    # settings.py
    JSONRPC_METHOD_MODULES = [
        # ...
        'your_app.rpc_methods',
    ]

.. code-block:: python

    # urls.py
    urlpatterns = [
        # ...
        path('rpc', JSONRPCView.as_view()),
    ]

.. code-block:: python

    # your_app/rpc_methods.py
    from bthlabs_jsonrpc_core import register_method

    @register_method(name='hello')
    def hello(request, who='World'):
        return f'Hello, {who}!'

Author
------

*bthlabs-jsonrpc-django* is developed by `Tomek Wójcik`_.

License
-------

*bthlabs-jsonrpc-django* is licensed under the MIT License.

.. _Docs: https://projects.bthlabs.pl/bthlabs-jsonrpc/django/
.. _Source repository: https://git.bthlabs.pl/tomekwojcik/bthlabs-jsonrpc/
.. _Tomek Wójcik: https://www.bthlabs.pl/
