from setuptools import setup

# reading long description from file
with open('README.md') as file:
    README = file.read()


# specify requirements of your package here
REQUIREMENTS = []

# some more details
CLASSIFIERS = [
    'Development Status :: 4 - Beta',
    'Intended Audience :: Developers',
    'Topic :: Internet',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python',
    'Programming Language :: Python :: 2',
    'Programming Language :: Python :: 2.6',
    'Programming Language :: Python :: 2.7',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
]

setup(
    name='wedeliver_migrate_manager',
    version='1.3',
    description='Migrate Manager for Services Database',
    url='https://www.wedeliverapp.com/',
    author='weDeliver',
    author_email='info@wedeliverapp.com',
    license='MIT',
    packages=['wedeliver_migrate_manager'],
    classifiers=CLASSIFIERS,
    install_requires=REQUIREMENTS,
    long_description_content_type="text/markdown",
    long_description=README,
)
