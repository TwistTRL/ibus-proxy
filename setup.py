from distutils.core import setup

setup(
    name='ibus-proxy',
    version='0.1.0',
    author='Lingyu Zhou',
    author_email='zhoulytwin@gmail.com',
    scripts=['bin/ibus-proxy.py'],
    url='https://github.com/TwistTRL/ibus-proxy',
    license='GPL-3.0',
    description='https://github.com/TwistTRL/ibus-proxy',
    install_requires=[
        "docopt >= 0.6.1",
    ],
)
