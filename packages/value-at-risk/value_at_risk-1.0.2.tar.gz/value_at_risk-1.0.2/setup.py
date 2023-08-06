from setuptools import setup

# Package meta-data.
NAME = 'value_at_risk'
DESCRIPTION = 'Value at Risk Calculator'
URL = 'https://github.com/moodoid/value_at_risk'
AUTHOR = 'moodoid'
REQUIRES_PYTHON = '>=3.6.0'
VERSION = '0.1.0'

setup(
    name='value_at_risk',
    version='1.0.2',
    author='moodoid',
    keywords='Value-at-Risk Tool',
    packages=['value_at_risk'],
    description='Value at Risk Calculator',
    long_description='Calculate Value-at-Risk (VaR) of a portfolio through historical and parametric methods',
    long_description_content_type='text/plain',
    url='https://github.com/moodoid/value_at_risk',
    classifiers=['Intended Audience :: Developers',
                 ]
)
