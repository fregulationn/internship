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
    name='face_fusion',
    version=__version__,
    author='junjie.zhang',
    author_email='iszhangjunjie@outlook.com',
    url='https://github.com/fregulationn/python-REST.git',
    description='人脸相关rest服务接口',
    packages=find_packages(),
    include_package_data=True,
    install_requires=get_requirements(),
    entry_points={
        'console_scripts': [
            'rest_face = rest.start_app:main'
        ],
    }
)
