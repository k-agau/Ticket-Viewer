from setuptools import setup

setup(
    name='TicketViewer',
    version='1.0',
    py_modules=['viewer'],
    install_requires=[
        'pycurl',
        'Click',
        'pyfiglet',
    ],
    entry_points='''
        [console_scripts]
        viewer=viewer:main
    ''',
)