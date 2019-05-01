from distutils.core import setup

setup(
    name='ibus_proxy',
    version='0.1.0',
    author='Lingyu Zhou',
    author_email='zhoulytwin@gmail.com',
    scripts=['bin/ibus_proxy.py'],
    url='',
    license='GPL-3.0',
    description='Useful towel-related stuff.',
    long_description=open('README.txt').read(),
    install_requires=[
        "docopt >= 0.6.1",
    ],
)
