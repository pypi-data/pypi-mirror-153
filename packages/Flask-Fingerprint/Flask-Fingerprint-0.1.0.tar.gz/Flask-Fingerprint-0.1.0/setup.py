import setuptools

# Load README
with open('README.md', 'r', encoding = 'utf8') as file:
    long_description = file.read()

# Define package metadata
setuptools.setup(
    name = 'Flask-Fingerprint',
    version = '0.1.0',
    author = 'Martin Folkers',
    author_email = 'hello@twobrain.io',
    description = 'Flask extension for fingerprinting static assets',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    url = 'https://codeberg.org/S1SYPHOS/flask-fingerprint',
    license = 'MIT',
    project_urls = {
        'Issues': 'https://codeberg.org/S1SYPHOS/flask-fingerprint/issues',
    },
    py_modules = ['flask_fingerprint'],
    packages = setuptools.find_packages(),
    include_package_data = True,
    install_requires = ['flask'],
    platforms = 'any',
    classifiers = [
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Framework :: Flask',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ],
    python_requires = '>= 3.7',
    zip_safe = False,
)
