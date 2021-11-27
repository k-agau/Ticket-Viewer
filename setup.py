from setuptools import setup

setup(
    name='TicketViewer',
    version='1.0',
    py_modules=['viewer'],
    install_requires=[
        'requests',
        'Click',
        'pyfiglet',
        'certifi',
        'termcolor',
        'six'
    ],
    entry_points='''
        [console_scripts]
        viewer=viewer:login
    ''',
)