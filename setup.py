from setuptools import setup, find_packages

INSTALL_REQUIRES = [
    'Flask>=0.10',
    'Flask-Babel>=0.9',
    'Flask-Login>=0.2',
    'Flask-Mail>=0.9',
    'Flask-Migrate>=1.3',
    'Flask-OpenID>=1.2',
    'Flask-RESTful>=0.3',
    'Flask-Script>=2.0',
    'Flask-SQLAlchemy>=2.0',
    'Flask-WhooshAlchemy>=0.56',
    'Flask-WTF>=0.11',
]

ENTRY_POINTS = dict(
    console_scripts=[
        'studreg = run:manager.run',
    ],
)

setup(
    name='studreg',
    version='0.1',
    long_description=__doc__,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    license='AGPL',
    author='Yuval Langer',
    author_email='yuval.langer@gmail.com',
    url='https://gitlab.com/agudaorgil/studreg/',
    install_requires=INSTALL_REQUIRES,
    entry_points=ENTRY_POINTS,
)
