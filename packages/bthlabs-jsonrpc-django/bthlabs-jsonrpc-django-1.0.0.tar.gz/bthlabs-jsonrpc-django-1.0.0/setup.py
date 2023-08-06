# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['bthlabs_jsonrpc_django']

package_data = \
{'': ['*']}

install_requires = \
['bthlabs-jsonrpc-core==1.0.0', 'django>=3.2,<5.0']

setup_kwargs = {
    'name': 'bthlabs-jsonrpc-django',
    'version': '1.0.0',
    'description': 'BTHLabs JSONRPC - Django integration',
    'long_description': "bthlabs-jsonrpc-django\n======================\n\nBTHLabs JSONRPC - django integration\n\n`Docs`_ | `Source repository`_\n\nOverview\n--------\n\nBTHLabs JSONRPC is a set of Python libraries that provide extensible framework\nfor adding JSONRPC interfaces to existing Python Web applications.\n\nThe *django* package provides Django integration.\n\nInstallation\n------------\n\n.. code-block:: shell\n\n    $ pip install bthlabs_jsonrpc_django\n\nExample\n-------\n\n.. code-block:: python\n\n    # settings.py\n    INSTALLED_APPS = [\n        # ...\n        'bthlabs_jsonrpc_django',\n    ]\n\n.. code-block:: python\n\n    # settings.py\n    JSONRPC_METHOD_MODULES = [\n        # ...\n        'your_app.rpc_methods',\n    ]\n\n.. code-block:: python\n\n    # urls.py\n    urlpatterns = [\n        # ...\n        path('rpc', JSONRPCView.as_view()),\n    ]\n\n.. code-block:: python\n\n    # your_app/rpc_methods.py\n    from bthlabs_jsonrpc_core import register_method\n\n    @register_method(name='hello')\n    def hello(request, who='World'):\n        return f'Hello, {who}!'\n\nAuthor\n------\n\n*bthlabs-jsonrpc-django* is developed by `Tomek Wójcik`_.\n\nLicense\n-------\n\n*bthlabs-jsonrpc-django* is licensed under the MIT License.\n\n.. _Docs: https://projects.bthlabs.pl/bthlabs-jsonrpc/django/\n.. _Source repository: https://git.bthlabs.pl/tomekwojcik/bthlabs-jsonrpc/\n.. _Tomek Wójcik: https://www.bthlabs.pl/\n",
    'author': 'Tomek Wójcik',
    'author_email': 'contact@bthlabs.pl',
    'maintainer': 'BTHLabs',
    'maintainer_email': 'contact@bthlabs.pl',
    'url': 'https://projects.bthlabs.pl/bthlabs-jsonrpc/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.10,<4.0',
}


setup(**setup_kwargs)
