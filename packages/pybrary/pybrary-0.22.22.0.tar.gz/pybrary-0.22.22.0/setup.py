from os.path import join, dirname, abspath

from setuptools import setup, find_packages

curdir = abspath(dirname(__file__))
readme = open(join(curdir, 'README.rst')).read()

setup(
    name             = 'pybrary',
    version          = '0.22.22.0',
    description      = 'Python Library',
    long_description = readme,
    keywords         = ['library', ],
    url              = 'https://framagit.org/louis-riviere-xyz/pybrary/tree/stable',
    author           = 'Louis RIVIERE',
    author_email     = 'louis@riviere.xyz',
    license          = 'MIT',
    classifiers      = [
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        "Operating System :: POSIX :: Linux",
        "Environment :: Console",
        'Intended Audience :: Developers',
    ],
    packages = find_packages(),
    install_requires = [
        'cryptography',
    ],
    entry_points = dict(
        console_scripts = (
            'pybrary=pybrary.main:main',
        ),
    ),
)
