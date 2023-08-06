import setuptools

# Load README
with open('README.md', 'r', encoding = 'utf8') as file:
    long_description = file.read()

# Define package metadata
setuptools.setup(
    name = 'gesetze',
    version = '1.1.1',
    author = 'Martin Folkers',
    author_email = 'hello@twobrain.io',
    description = '',
    long_description = long_description,
    long_description_content_type = 'text/markdown',
    url = 'https://codeberg.org/S1SYPHOS/py-gesetze',
    license = 'MIT',
    project_urls = {
        'Issues': 'https://codeberg.org/S1SYPHOS/py-gesetze/issues',
    },
    entry_points = """
        [console_scripts]
        gesetze=gesetze.cli:cli
    """,
    classifiers = [
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    packages = setuptools.find_packages(),
    package_data = {'gesetze': ['data/*.json']},
    install_requires = [
        'bs4',
        'click',
        'lxml',
        'requests',
    ],
    python_requires = '>= 3.6'
)
