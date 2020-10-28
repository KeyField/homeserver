from setuptools import setup, find_packages

with open("keyfieldhome/__init__.py") as f:
    version = next(l.split('"')[-2] for l in f if l.startswith('__version__'))

with open("README.md", "r") as f:
    readme = f.read()

setup(
    name='KeyField Homeserver',
    version=version,
    description="The KeyField reference Homeserver implementation",
    long_description=readme,
    long_description_content_type="text/markdown",
    classifiers=[], # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
    keywords='keyfield federation crypto chat',
    author='Ben Klein',
    author_email='robobenklein@gmail.com',
    url='https://keyfield.io/',
    license='MPL-2.0',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests', 'venv']),
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "flask",
        "coloredlogs",
        "pymongo",
        "toml",
        "gunicorn",
        "requests",
        "mongoengine",
        "bcrypt",
        "pytz",
        "msgpack",
        "pynacl",
    ],
    entry_points={
        'console_scripts': [
            'keyfield-homeserver=keyfieldhome.__main__:__main__'
        ]
    },
    python_requires='>=3.7'
)
