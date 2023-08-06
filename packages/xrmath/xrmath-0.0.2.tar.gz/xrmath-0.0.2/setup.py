from setuptools import find_packages, setup
 
# Package meta-data.
NAME = 'xrmath'
DESCRIPTION = 'A math tool by Xinre.'
URL = 'https://github.com/Dingchina2020/xrmath.git'
EMAIL = 'ancdngding@qq.com'
AUTHOR = 'Xinre'
REQUIRES_PYTHON = '>=3.6.0'
VERSION = '0.0.2'

# What packages are required for this module to be executed?
REQUIRED = []

# Setting.
setup(
    name=NAME,
    version=VERSION,
    description=DESCRIPTION,
    author=AUTHOR,
    python_requires=REQUIRES_PYTHON,
    url=URL,
    packages=find_packages(),
    install_requires=REQUIRED,
    license="MIT"
)
