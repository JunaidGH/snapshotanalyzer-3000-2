from setuptools import setup

setup(
    name='snapshotanalyzer-3000-2',
    version='0.1',
    author="Junaid Mohammad",
    description="snapshotanalyzer-3000-2 is a tool to manage EC2",
    licemse="GPLv3+",
    packages=['shotty'],
    url="https://github.com/JunaidGH/snapshotanalyzer-3000-2",
    install_requires=[
        'click',
        'boto3'
    ],
    entry_points='''
        [console_scripts]
        shotty=shotty.shotty:cli
        ''',
)
