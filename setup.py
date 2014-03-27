from setuptools import setup

setup(
    name='deploy',
    version='0.0.1',
    packages=['deploy', 'deploy.lib'],
    url='http://www.studio-donder.nl/',
    license='MIT',
    author='Marijn Giesen',
    author_email='marijn@studio-donder.nl',
    description='Deploy - our deploy tool',
    entry_points={
        'console_scripts': [
            'deployd = deploy.main:main',
        ]
    },
    requires=['requests', 'pygit2']
)
