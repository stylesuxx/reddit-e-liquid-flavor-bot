from distutils.core import setup

setup(
    name='flavor_bot',
    version='0.0.3',
    description='Post links to flavors mentioned in posts.',
    long_description=open('README.md').read(),
    author='Chris Landa',
    author_email='stylesuxx@gmail.com',
    url='https://github.com/stylesuxx/reddit-e-liquid-flavor-bot',
    license='MIT',
    packages=['flavor_bot'],
    scripts=['flavorBot', 'OAuth'])
