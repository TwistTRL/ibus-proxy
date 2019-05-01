from distutils.core import setup

setup(
    name='ibus_proxy',
    version='0.1.0',
    author='Lingyu Zhou',
    author_email='zhoulytwin@gmail.com',
    scripts=['bin/ibus_proxy.py'],
    url='https://github.com/TwistTRL/ibus_proxy',
    license='GPL-3.0',
    description='https://github.com/TwistTRL/ibus_proxy',
    install_requires=[
        "docopt >= 0.6.1",
    ],
)
