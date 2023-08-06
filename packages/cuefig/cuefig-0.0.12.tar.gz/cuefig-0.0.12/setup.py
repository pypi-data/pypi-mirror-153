import os
import sys

from setuptools import setup, find_packages, Command

__PATH__ = os.path.abspath(os.path.dirname(__file__))
__version__ = "0.0.12"


def read_readme():
    with open('README.md', mode="r", encoding="utf8") as f:
        return f.read()


# brought from https://github.com/kennethreitz/setup.py
class DeployCommand(Command):
    description = 'Build and deploy the package to PyPI.'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    @staticmethod
    def status(s):
        print(s)

    def run(self):
        import twine  # we require twine locally  # noqa

        assert 'dev' not in __version__, (
            "Only non-devel versions are allowed. "
            "__version__ == {}".format(__version__))

        with os.popen("git status --short") as fp:
            git_status = fp.read().strip()
            if git_status:
                print("Error: git repository is not clean.\n")
                os.system("git status --short")
                sys.exit(1)

        try:
            from shutil import rmtree
            self.status('Removing previous builds ...')
            rmtree(os.path.join(__PATH__, 'dist'))
        except OSError:
            pass

        self.status('Building Source and Wheel (universal) distribution ...')
        os.system('{0} setup.py sdist'.format(sys.executable))

        self.status('Uploading the package to PyPI via Twine ...')
        ret = os.system('twine upload --repository pypi dist/*')
        if ret != 0:
            sys.exit(ret)

        self.status('Creating git tags ...')
        os.system('git tag v{0}'.format(__version__))
        os.system('git tag --list')
        sys.exit()


install_requires = ["PyYAML>=6.0"]

setup(
    name='cuefig',
    version=__version__,
    url='https://github.com/FavorMylikes/cuefig',
    license='MIT License',
    author='麦丽素',
    author_email='l786112323@gmail.com',
    description='A config framework that you can cue and hint quickly.',
    long_description=read_readme(),
    long_description_content_type='text/markdown',
    package_data={"": ["*.yaml"], },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=install_requires,
    packages=find_packages(),
    python_requires=">=3.7",
    entry_points={
        'console_scripts': ['cuefig=cli:main'],
    },
    cmdclass={
        'deploy': DeployCommand,
    },
    include_package_data=True,
)
