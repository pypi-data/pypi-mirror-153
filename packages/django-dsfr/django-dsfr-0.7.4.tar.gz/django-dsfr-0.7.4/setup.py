# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['dsfr', 'dsfr.migrations', 'dsfr.templatetags', 'dsfr.test']

package_data = \
{'': ['*'],
 'dsfr': ['fixtures/*',
          'static/dsfr/dist/artwork/*',
          'static/dsfr/dist/component/*',
          'static/dsfr/dist/component/accordion/*',
          'static/dsfr/dist/component/alert/*',
          'static/dsfr/dist/component/badge/*',
          'static/dsfr/dist/component/breadcrumb/*',
          'static/dsfr/dist/component/button/*',
          'static/dsfr/dist/component/callout/*',
          'static/dsfr/dist/component/card/*',
          'static/dsfr/dist/component/checkbox/*',
          'static/dsfr/dist/component/connect/*',
          'static/dsfr/dist/component/consent/*',
          'static/dsfr/dist/component/content/*',
          'static/dsfr/dist/component/display/*',
          'static/dsfr/dist/component/follow/*',
          'static/dsfr/dist/component/footer/*',
          'static/dsfr/dist/component/form/*',
          'static/dsfr/dist/component/header/*',
          'static/dsfr/dist/component/highlight/*',
          'static/dsfr/dist/component/input/*',
          'static/dsfr/dist/component/link/*',
          'static/dsfr/dist/component/logo/*',
          'static/dsfr/dist/component/modal/*',
          'static/dsfr/dist/component/navigation/*',
          'static/dsfr/dist/component/pagination/*',
          'static/dsfr/dist/component/quote/*',
          'static/dsfr/dist/component/radio/*',
          'static/dsfr/dist/component/search/*',
          'static/dsfr/dist/component/select/*',
          'static/dsfr/dist/component/share/*',
          'static/dsfr/dist/component/sidemenu/*',
          'static/dsfr/dist/component/skiplink/*',
          'static/dsfr/dist/component/summary/*',
          'static/dsfr/dist/component/tab/*',
          'static/dsfr/dist/component/table/*',
          'static/dsfr/dist/component/tag/*',
          'static/dsfr/dist/component/tile/*',
          'static/dsfr/dist/component/toggle/*',
          'static/dsfr/dist/component/upload/*',
          'static/dsfr/dist/core/*',
          'static/dsfr/dist/dsfr/*',
          'static/dsfr/dist/favicon/*',
          'static/dsfr/dist/fonts/*',
          'static/dsfr/dist/legacy/*',
          'static/dsfr/dist/page/*',
          'static/dsfr/dist/pattern/*',
          'static/dsfr/dist/scheme/*',
          'templates/dsfr/*']}

install_requires = \
['Django>=3.2.5,<4.0.0', 'requests>=2.26.0,<3.0.0']

setup_kwargs = {
    'name': 'django-dsfr',
    'version': '0.7.4',
    'description': 'Integrate the French government Design System into a Django app',
    'long_description': '.. image:: https://badge.fury.io/py/django-dsfr.svg\n    :target: https://pypi.org/project/django-dsfr/\n\n.. image:: https://github.com/entrepreneur-interet-general/django-dsfr/actions/workflows/django.yml/badge.svg\n    :target: https://github.com/entrepreneur-interet-general/django-dsfr/actions/workflows/django.yml\n\n.. image:: https://github.com/entrepreneur-interet-general/django-dsfr/actions/workflows/codeql-analysis.yml/badge.svg\n    :target: https://github.com/entrepreneur-interet-general/django-dsfr/actions/workflows/codeql-analysis.yml\n\n\n===========\nDjango-DSFR\n===========\n\nDjango-DSFR is a Django app to integrate the `French government Design System ("Système de design de l’État français") <https://www.systeme-de-design.gouv.fr/>`_.\n\n\nThis app was created as a part of `Open Collectivités <https://github.com/entrepreneur-interet-general/opencollectivites>`_ and is very much a work in progress. See the `documentation (in French) <https://entrepreneur-interet-general.github.io/django-dsfr/>`_ for details.\n\nDjango-DSFR (partly) implements the `version 1.4 of the DSFR <https://gouvfr.atlassian.net/wiki/spaces/DB/pages/978354177/Version+1.4>`_.\n\nRequirements\n------------\nTested with Python 3.7 to 3.10 and Django 3.2.5 to 3.2.13. Per `vermin <https://github.com/netromdk/vermin>`_, it should work with Python >= 3.0, and it should work with old versions of Django too.\n\nQuick start\n-----------\n\n1. Install with :code:`pip install django-dsfr`.\n\n2. Add "dsfr" to INSTALLED_APPS in your settings.py like this, before the app you want to use it with::\n\n    INSTALLED_APPS = [\n        ...\n        \'dsfr\',\n        <your_app>\n    ]\n\n3. (Optional) Add the context processor to your settings.py and create an instance of "DsfrConfig" in the admin panel::\n\n    TEMPLATES = [\n        {\n            [...]\n            "OPTIONS": {\n                "context_processors": [\n                    [...]\n                    "dsfr.context_processors.site_config",\n                ],\n            },\n        },\n    ]\n\n\n4. Include the tags in your base.html file (see example file at https://github.com/entrepreneur-interet-general/django-dsfr/blob/main/example_app/templates/example_app/base.html)\n\n5. Start the development server and visit http://127.0.0.1:8000/\n',
    'author': 'Sylvain Boissel',
    'author_email': 'sylvain.boissel@dgcl.gouv.fr',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/entrepreneur-interet-general/django-dsfr',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
