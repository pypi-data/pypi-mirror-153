
from setuptools import setup, find_packages


with open('requirements.txt') as f:
    requires = f.read().splitlines()

__version__ = '0.1.2'

url = 'https://github.com/pmaigutyak/mp-delivery'


setup(
    name='django-mp-delivery',
    version=__version__,
    description='Django delivery app',
    author='Paul Maigutyak',
    author_email='pmaigutyak@gmail.com',
    url=url,
    download_url='%s/archive/%s.tar.gz' % (url, __version__),
    packages=find_packages(),
    include_package_data=True,
    license='MIT',
    install_requires=requires
)
