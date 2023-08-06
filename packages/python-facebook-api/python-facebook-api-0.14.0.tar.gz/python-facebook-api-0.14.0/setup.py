# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['pyfacebook',
 'pyfacebook.api',
 'pyfacebook.api.facebook',
 'pyfacebook.api.facebook.common_edges',
 'pyfacebook.api.facebook.resource',
 'pyfacebook.api.instagram_basic',
 'pyfacebook.api.instagram_basic.resource',
 'pyfacebook.api.instagram_business',
 'pyfacebook.api.instagram_business.resource',
 'pyfacebook.models',
 'pyfacebook.utils',
 'tests',
 'tests.facebook',
 'tests.instagram_basic',
 'tests.instagram_business',
 'tests.utils']

package_data = \
{'': ['*']}

install_requires = \
['dataclasses-json>=0.5.4,<0.6.0',
 'requests-oauthlib>=1.3.0,<2.0.0',
 'requests>=2.24.0,<3.0.0']

setup_kwargs = {
    'name': 'python-facebook-api',
    'version': '0.14.0',
    'description': 'A simple Python wrapper around the Facebook Graph API',
    'long_description': 'Python Facebook\n\nA Python wrapper for the Facebook Common API.\n\n.. image:: https://github.com/sns-sdks/python-facebook/workflows/Test/badge.svg\n    :target: https://github.com/sns-sdks/python-facebook/actions\n    :alt: Build Status\n\n.. image:: https://img.shields.io/badge/Docs-passing-brightgreen\n    :target: https://sns-sdks.github.io/python-facebook/\n    :alt: Documentation Status\n\n.. image:: https://codecov.io/gh/sns-sdks/python-facebook/branch/master/graph/badge.svg\n    :target: https://codecov.io/gh/sns-sdks/python-facebook\n    :alt: Codecov\n\n.. image:: https://img.shields.io/pypi/v/python-facebook-api.svg\n    :target: https://pypi.org/project/python-facebook-api\n    :alt: PyPI\n\n\n============\nIntroduction\n============\n\nWe have refactored this library after v0.10.0. If you want to use old version, please see branch ``v0``.\n\nThe new structure we will provide like follow show.\n\n.. image:: docs/docs/images/structure.png\n\n\n.. note::\n\n    This new structure still in developing.\n\n    Now You can use base class ``GraphApi`` to get data.\n\n==========\nInstalling\n==========\n\nIf you want to use old version you can set version to ``0.9.*``, And this series will also support with python2.7\n\nYou can install this library from ``pypi``::\n\n    $pip install --upgrade python-facebook-api\n    ✨🍰✨\n\n\n=====\nUsage\n=====\n\n--------\nGraphAPI\n--------\n\nNow you can use ``GraphApi`` class to communicate with Facebook Graph Api.\n\nYou can initial ``GraphApi`` with three different methods.\n\n1. if you already have an access token, you can initial with it::\n\n    >>> from pyfacebook import GraphAPI\n    >>> api = GraphAPI(access_token="token")\n\n2. if you want to use app credentials to generate app token::\n\n    >>> from pyfacebook import GraphAPI\n    >>> api = GraphAPI(app_id="id", app_secret="secret", application_only_auth=True)\n\n3. if you want to perform an authorization process to a user::\n\n    >>> from pyfacebook import GraphAPI\n    >>> api = GraphAPI(app_id="id", app_secret="secret", oauth_flow=True)\n    >>> api.get_authorization_url()\n    # (\'https://www.facebook.com/dialog/oauth?response_type=code&client_id=id&redirect_uri=https%3A%2F%2Flocalhost%2F&scope=public_profile&state=PyFacebook\', \'PyFacebook\')\n    # let user to do oauth at the browser opened by link.\n    # then get the response url\n    >>> api.exchange_user_access_token(response="url redirected")\n    # Now the api will get the user access token.\n\nThen you can get data from facebook.\n\nGet object data::\n\n    >>> api.get_object(object_id="20531316728")\n    >>> {\'name\': \'Facebook App\', \'id\': \'20531316728\'}\n\nMore you can see the code because we still working on new structure.\n\n-----------\nFacebookAPI\n-----------\n\nInitial methods same with ``GraphAPI``.\n\nGet user data::\n\n    >>> fb.user.get_info(user_id="413140042878187")\n    >>> User(id=\'413140042878187\', name=\'Kun Liu\')\n\nGet page data::\n\n    >>> fb.page.get_info(page_id="20531316728")\n    >>> Page(id=\'20531316728\', name=\'Facebook App\')\n\nSee more in documents.\n\n========\nFeatures\n========\n\n\nNow library has cover follows features\n\nFacebook Graph API:\n\n- Application and Application\'s edges\n- Page and Page\'s edges\n- User and User\'s edges\n- Group and Group\'s edges\n- Event and Event\'s edges\n\nIG Business Graph API:\n\n- User and User\'s edges\n- Media and Media\'s edges\n\nIG Basic Display API:\n\n- User and User\'s edges\n- Media and Media\'s edges\n\n=======\nSUPPORT\n=======\n\n``python-facebook-api`` had been being developed with Pycharm under the free JetBrains Open Source license(s) granted by JetBrains s.r.o.,\nhence I would like to express my thanks here.\n\n.. image:: docs/docs/images/jetbrains.svg\n    :target: https://www.jetbrains.com/?from=sns-sdks/python-facebook\n    :alt: Jetbrains\n',
    'author': 'Ikaros kun',
    'author_email': 'merle.liukun@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/sns-sdks/python-facebook',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
