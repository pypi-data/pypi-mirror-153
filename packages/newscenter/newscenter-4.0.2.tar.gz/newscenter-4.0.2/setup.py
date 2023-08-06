# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['newscenter', 'newscenter.migrations', 'newscenter.templatetags']

package_data = \
{'': ['*'],
 'newscenter': ['static/newscenter/css/*',
                'static/newscenter/img/*',
                'static/newscenter/js/*',
                'static/newscenter/js/bxslider/*',
                'static/newscenter/js/bxslider/images/*',
                'static/newscenter/js/bxslider/plugins/*',
                'static/newscenter/js/popeye/*',
                'static/newscenter/js/popeye/img/*',
                'templates/newscenter/*',
                'templates/newscenter/includes/*']}

install_requires = \
['Pillow>=9.0.0,<10.0.0',
 'django-el-pagination>=3.0.0,<4.0.0',
 'easy-thumbnails>=2.8.0,<3.0.0',
 'feedparser>=6.0.0,<7.0.0',
 'site-config>=2.0.0,<3.0.0']

setup_kwargs = {
    'name': 'newscenter',
    'version': '4.0.2',
    'description': 'A News Release Application for Django',
    'long_description': '=================\nDjango Newscenter\n=================\n\nA Django application for creating news releases which can be associated with unique newsroom objects.\n\nA Django CMS apphook is included as well as a templatetag for rendering news release headlines in non-application templates.\n\n\nInstallation\n============\n\nAdd newscenter to your python path:\n\n    $ pip install newscenter\n\nAdd the following to the INSTALLED_APPS of your project\'s settings.py:\n\n    \'newscenter\',\n\nIn your urls.py, add:\n    url(r\'^newscenter/\', include(\'newscenter.urls\')),\n\nRun:\n\n   ``manage.py migrate``\n\nCollect static media:\n\n   ``manage.py collectstatic``\n\n\nDependencies\n============\n\nThe following will be installed automatically if you use pip to install newscenter:\n\n    Pillow (http://python-pillow.github.io/)\n\n    easy-thumbnails (https://github.com/SmileyChris/easy-thumbnails)\n\n    feedparser (http://pythonhosted.org/feedparser/)\n\n    django-el-pagination (https://django-el-pagination.readthedocs.io/en/latest/start.html)\n\nFor easy-thumbnails, you\'ll also need to add it to INSTALLED_APPS and run migrate:\n    \'easy_thumbnails\',\n\nFor django-el-pagination, you\'ll also need to add it to INSTALLED_APPS:\n    \'el_pagination\',\n\nYou will also need to update your `context_processors` with:\n    \'django.template.context_processors.request\',\n\nNB: don\'t forget to delete any \'endless_pagination\' from   INSTALLED_APPS in the settings.py file.\n\nTemplate Tag\n============\n\nThe template tag can be used like this::\n\n    {% load newscenter_tags %}\n    {% get_news "newsroom-name" %}\n    <h1><a href="{{ newsroom.get_absolute_url }}">{{ newsroom.name }}</a></h1>\n    {% for release in featured_list %}\n    <article>\n    <h2>{{ release.title }}</h2>\n    <p class="teaser">{{ release.teaser }}</p>\n    <p><a href="{{ release.get_absolute_url }}">Read more</a></p>\n    </article>\n    {% endfor %}\n\n\nChange Log\n============\n3.0.1:\n\n- Compatible with Django 3.2, Python 3.9\n\n2.0.14:\n\n- django-endless-pagination -> django-el-pagination\n\nChanged in 2.0.0:\n\n- In this version, we changed the name of the migrations directories as follows. If you are using Django 1.7+ and are upgrading to newscenter 2.0.0, you can make sure to remove newscenter from MIGRATION_MODULES in settings.py. If you are using Django 1.6, update the MIGRATION_MODULES as documented above.\n\n- https://github.com/ImaginaryLandscape/django-newscenter/issues/4\n\n\nRenamed Directories:\nmigrations -> south_migrations\nmigrations_django -> migrations\n\n- Fixed a depreciation warning in forms.py regarding get_model\n\n- https://github.com/ImaginaryLandscape/django-newscenter/issues/3\n\nNew in 1.5.8:\n- Added support for Django 1.7\n\nNew in 1.4.1:\n- Added title field to Contact model\n\nNew in 1.4:\n- Switched image plugin from popeye to bxslider\n',
    'author': 'Imaginary Landscape',
    'author_email': 'info@imagescape.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ImaginaryLandscape/django-newscenter',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
