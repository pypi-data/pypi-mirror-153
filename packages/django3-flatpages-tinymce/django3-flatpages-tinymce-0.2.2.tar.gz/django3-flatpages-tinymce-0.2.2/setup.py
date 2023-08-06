# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['flatpages_tinymce', 'flatpages_tinymce.templatetags']

package_data = \
{'': ['*'],
 'flatpages_tinymce': ['static/flatpages_tinymce/*',
                       'templates/flatpages_tinymce/*']}

install_requires = \
['Django>=3.0', 'django_tinymce>=1.5']

setup_kwargs = {
    'name': 'django3-flatpages-tinymce',
    'version': '0.2.2',
    'description': 'HTML editor on django.contrib.flatpages',
    'long_description': '# About\n\n**django3-flatpages-tinymce** provides on-site editing of "Flat Pages"\nwith minimal impact on the rest of code.  This is a fork of the original,\ndropping support for python 2 and django < 3.0.\n\ndjango3-flatpages-tinymce is available under the MIT license.\n\n# Usage\n\nFirst of all, you need to have **django3-flatpages-tinymce** and\n**django-tinymce** installed; for your convenience, recent versions\nshould be available from PyPI.\n\n    pip install django-tinymce django3-flatpages-tinymce\n\nTo use, just add these applications to your INSTALLED_APPS **after**\n**django.contrib.flatpages** app:\n\n    INSTALLED_APPS = (\n        ...\n            \'django.contrib.staticfiles\',\n            \'django.contrib.flatpages\',\n            ...\n            \'tinymce\',\n            \'flatpages_tinymce\',\n    )\n\nAs instructed by the **flatpages** guide, add this to your\nMIDDLEWARE_CLASSES:\n\n    MIDDLEWARE_CLASSES = (\n        ...\n        \'django.contrib.flatpages.middleware.FlatpageFallbackMiddleware\',\n    )\n\nRemember that this little addition to your **urls.py** is required by\n**django-tinymce**:\n\n    urlpatterns = patterns(\'\',\n        ...\n        path(\'tinymce/\', include(\'tinymce.urls\')),\n        ...\n    )\n\nFinally create the tables for **flatpages** and install the JS/CSS files\nusing\n\n    ./manage.py nugrate\n    ./manage.py collectstatic\n\nIf you want on-site editing of templates, you must edit **flatpages**\ntemplates: change {{flatpage.content} to {% flatpage_admin flatpage %}\nfrom flatpage_admin template library. So\n\n    {% extends "base.html" %}\n    {% block body %}\n    {% endblock %}\n    {% block body %}\n    <h1>{{flatpage.title}}</h1>\n    {{flatpage.content}}\n    {% endblock %}\n\nwill become\n\n    {% extends "base.html" %}\n    {% load flatpage_admin %}\n    {% block body %}\n    <h1>{{flatpage.title}}</h1>\n    {% flatpage_admin flatpage %]\n    {% endblock %}\n\nIf you are bothered with \\<script\\>/\\<link\\> tags, being inserted in\n\\<body\\> tag and your template has something like {% block extrahead %},\nyou can move all plugin media in head, using {% flatpage_media %} tag.\n\n    {% extends "base.html" %}\n    {% block extrahead %}\n    {% flatpage_media %}\n    {% endblock %}\n    {% block body %}\n    <h1>{{flatpage.title}}</h1>\n    {% flatpage_admin flatpage %}\n    {% endblock %}\n\n# Settings\n\nDefault settings are in flatpages_tinymce.settings.py file. Also, you\ncan override them in site-wide settings.py file. The main of them are:\n\n> -   FLATPAGES_TINYMCE_ADMIN (default True) - use TinyMCE widget in\n>     admin area\n> -   FLATPAGES_TINYMCE_FRONTEND (default True) - use TinyMCE widget in\n>     frontend\n> -   FLATPAGES_TEMPLATE_DIR (default: TEMPLATE_DIRS\\[0\\] +\n>     \'flatpages\') - directory where flatpages templates are placed\n> -   FLATPAGES USE_MINIFIED (defalut: not settings.DEBUG) - use\n>     minified versions of JS/CSS\n\nFurther, you will want to change default settings of TinyMCE Editor.\n\n    TINYMCE_DEFAULT_CONFIG = {\n       # custom plugins\n           \'plugins\': "table,spellchecker,paste,searchreplace",\n       # editor theme\n       \'theme\': "advanced",\n       # custom CSS file for styling editor area\n           \'content_css\': MEDIA_URL + "css/custom_tinymce.css",\n           # use absolute urls when inserting links/images\n           \'relative_urls\': False,\n       }\n\n# Changes\n\n## Changes in version 0.2\n\n> -   Ported to support Django \\> 3 and Python 3\n> -   drop support for Russian\n\n## Changes in version 0.1\n\n> -   First public release.\n',
    'author': 'Scott Sharkey',
    'author_email': 'ssharkey@lanshark.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/lansharkconsulting/django/django3-flatpages-tinymce',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
