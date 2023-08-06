from setuptools import setup

setup(
    name='zephony_helpers',
    packages=['zephony_helpers'],
    description='Helper functions for Python web development',
    version='0.2',
    url='https://github.com/Zephony/helpers',
    author='Kevin Isaac',
    author_email='kevin@zephony.com',
    keywords=['zephony', 'helpers', 'web'],
    install_requires=[
        'voluptuous',
        'twilio',
    ],
)

