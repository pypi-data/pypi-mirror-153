
from __future__ import print_function
from setuptools import setup, find_packages
import sys
magic_package_choice = 'python-magic-bin==0.4.14' if sys.platform.startswith("win") else 'python-magic==0.4.24'

# def read_file(filename):
#     with open(filename) as fp:
#         return fp.read().strip()
#
# def read_requirements(filename):
#     return [line.strip() for line in read_file(filename).splitlines()
#             if not line.startswith('#')]

# REQUIRED = read_requirements('requirements.txt')
setup(
    name='ImgAlter',
    version='0.1.7',
    author='White.tie',
    author_email='1042798703@qq.com',
    url='https://github.com/tyj-1995',
    description='1.Resize the image, 2.image transfer pdf',
    long_description='1.修改图片大小, 2.图片转成pdf',
    packages=['ImgAlter'],
    install_requires=["pillow>=8.0.1",
                      magic_package_choice],
    classifiers=[
        "Environment :: Web Environment",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Topic :: Text Processing :: Indexing",
        "Topic :: Utilities",
        "Topic :: Internet",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 3.6",
        ],
)
