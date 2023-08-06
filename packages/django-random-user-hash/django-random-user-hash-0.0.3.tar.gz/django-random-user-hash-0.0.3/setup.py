from setuptools import setup, find_packages


setup(
    name='django-random-user-hash',
    version='0.0.3',
    license='MIT',
    author="Av1dus",
    author_email='',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    url='https://github.com/Av1dus/django-random-user-hash',
    keywords='django hash user CTF',
    install_requires=[],
)