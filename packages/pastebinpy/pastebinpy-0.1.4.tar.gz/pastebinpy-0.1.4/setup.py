# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pastebinpy']

package_data = \
{'': ['*']}

setup_kwargs = {
    'name': 'pastebinpy',
    'version': '0.1.4',
    'description': 'A Pastebin api created in python with easy to use syntax',
    'long_description': 'PasteBinPy\n==========\nPasteBinPy\n    An easy to learn, use, and contribute to api for python.\n\n--------------\n\nGetting Started\n---------------\n\n    To get your pastebin api key, create or login to your pastebin account `here <https://pastebin.com/signup>`__ > after creating your account, `head over to the api documentation <https://pastebin.com/doc_api>`__ and grab your api key under ``Your Unique Developer API Key`` ---\n\nExample\n-------\n\n.. code:: py\n\n    import pastebinpy as pbp\n\n    # All thats needed for a successfull response\n    pbp.paste("api_key", "title", "body")\n\n    pbp.paste("api_key", "title", "body", raw=1, expiry="10M", privacy="1", format="python")\n\n``pastebinpy.paste()``\n----------------------\n\n**API\\_KEY** can be retrieved by making a pastebin account and getting your api key from `this link <https://pastebin.com/doc_api>`__\n\n**CONTENT** is the *body* of the paste, the inside that your user will be looking at.\n\n**TITLE** is at the top of the paste, users will probably not notice this, but its a good attribute to still use.\n\n**PRIVACY** has two values, ``0`` being public, and ``1`` being unlisted, meaning only people with the pastebin link can view it.\n\n**EXPIRY** is defining the expiration time and/or time limit that you give your paste. Allowed variables are below.\n\n::\n\n    N = Never\n    10M = 10 Minutes\n    1H = 1 Hour\n    1D = 1 Day\n    1W = 1 Week\n    2W = 2 Weeks\n    1M = 1 Month\n    6M = 6 Months\n    1Y = 1 Year\n\n**RAW** is the toggle attribute for obtaining a raw pastebin link, with ``1`` equaling the raw pastebin link, and ``0`` being the default, returning the normal pastebin link.\n\n**FORMAT** is the selected language attribute to format and color the content given. ``(e.g HTML, PHP, LUA, PYTHON, BF, CSS, CPP, CSHARP, RUBY, RAILS, etc)``\n\n--------------\n\nCreated by css / cesiyi',
    'author': 'Cesiyi',
    'author_email': 'css@amogus.cloud',
    'maintainer': 'Cesiyi',
    'maintainer_email': 'css@amogus.cloud',
    'url': None,
    'packages': packages,
    'package_data': package_data,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
