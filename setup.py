try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


config = {
    'description': 'Tool to start a project in Django 1.6 by automaing the yak shaving.',
    'author': 'Prabakaran Santhanam',
    'url': '',
    'download_url': '',
    'author_email': 'praba230890@gmail.com',
    'version': '0.01',
    'install_requires': [''],
    'packages': ['djangoyakshave'],
    'scripts': ['djangoyakshave/django-yak-shave.py'],
    'name': 'Django 1.6 Yak Shaving'
}

setup(**config)