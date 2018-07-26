"""Setup for python."""
from setuptools import setup, find_packages

FILE_VERSION = u'version.txt'
with open(FILE_VERSION) as f:
    __version__ = f.readline().splitlines()[0]


def get_requirements():
    """Get python requirement packages."""
    with open('./requirements.txt') as requirements:
        return [line.split('#', 1)[0].strip() for line in requirements
                if line and not line.startswith(('#', '--'))],


setup(
    name='intelli_extract_sentence',
    version=__version__,
    author='peng.he',
    author_email='peng.he@msxf.com',
    url='http://gitlab.msxf.com/peng.he/intelli-extract-sentence.git',
    description='智能保顾句子识别库',
    packages=find_packages(),
    include_package_data=True,
    install_requires=get_requirements(),
    entry_points={
        'console_scripts': [
            'ie-sentence = sentence.start_app:main'
        ],
    }
)
