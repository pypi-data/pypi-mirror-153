import os
import sys

from setuptools import setup, find_packages, Command
from shutil import rmtree
from kernel import __version__, __description__, __title__, __url__, __author__, __author_email__, __license__


HERE = os.path.abspath(os.path.dirname(__file__))
# Get the long description from the README file
with open(os.path.join(HERE, "README.md"), encoding="utf-8") as f:
    long_description = f.read()


class ParserCommand(Command):
    """Support setup.py upload."""
    ...

    def run(self):
        try:
            self.status('Removing previous builds ...')
            rmtree(os.path.join(HERE, 'dist'))
        except OSError:
            pass

        self.status('Building Source and Wheel (universal) distribution ...')
        os.system('{0} setup.py sdist bdist_wheel --universal'.format(sys.executable))

        self.status('Uploading the package to PyPI via Twine ...')
        os.system('twine upload dist/*')

        self.status('Pushing git tag ...')
        os.system('git tag v{0}'.format(__version__))
        os.system('git push --tags')

        sys.exit(0)


setup(
    name=__title__,
    version=__version__,
    description=__description__,
    long_description=f'Just Enjoy:{long_description}',
    classifiers=[
        # Get strings from http://pypi.python.org/pypi?%3Aaction=list_classifiers
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: Apache Software License",
        # supported python versions
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
        "Topic :: Software Development :: Libraries",
      ],
    keywords='python httpRunner terminal  swagger',
    author=__author__,
    author_email=__author_email__,
    url=__url__,
    license=__license__,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=True,
    install_requires=[
        'requests',
        'httprunner==2.5.7',
        'loguru',
        'PyYAML'
      ],
    entry_points={
        'console_scripts': [
            'doc2case = kernel.cli:mainRun'
        ]
      },
    cmdclass={
            'kernel': ParserCommand
        }
)

print("\nWelcome to Comet!")
print("If you have any questions, please visit our documentation page: {}\n".format(__url__))
