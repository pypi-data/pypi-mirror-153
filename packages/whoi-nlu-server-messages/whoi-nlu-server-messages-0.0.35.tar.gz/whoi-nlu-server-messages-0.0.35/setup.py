import sys
from distutils.core import setup


def get_version(filename):
    import ast
    version = None
    with open(filename) as f:
        for line in f:
            if line.startswith('__version__'):
                version = ast.parse(line).body[0].value.s
                break
        else:
            raise ValueError('No version found in %r.' % filename)
    if version is None:
        raise ValueError(filename)
    return version


lib_version = get_version(filename='include/whoi_nlu_server_messages/__init__.py')

setup(
    name='whoi-nlu-server-messages',
    packages=[
        'whoi_nlu_server_messages'
    ],
    package_dir={
        'whoi_nlu_server_messages': 'include/whoi_nlu_server_messages'
    },
    version=lib_version,
    license='MIT',
    description='whoi nlu server messages',
    author='Andrea F. Daniele',
    author_email='afdaniele@ttic.edu',
    url='https://github.com/ripl/whoi-nui-server-messages',
    keywords=['whoi', 'nlu'],
    install_requires=[
        'cbor2',
        *(['dataclasses'] if sys.version_info < (3, 7) else [])
    ],
    classifiers=[]
)
