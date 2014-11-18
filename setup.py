try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


config = {
    'description': 'Tool to start a project in Django 1.6 by automaing the yak shaving.',
    'author': 'Prabakaran Santhanam',
    'url': 'https://github.com/praba230890/djangoyakshave/',
    'license': 'Apache License',
    'author_email': 'praba230890@gmail.com',
    'version': '0.01',
    'install_requires': ['Django==1.6'],
    'packages': ['djangoyakshave', 'tests'],
    'scripts': ['djangoyakshave/django-yak-shave.py'],
    'name': 'Django 1.6 Yak Shaving'
}

setup(**config)
