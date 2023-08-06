from setuptools import setup, find_packages

from os import path


def read_from_file(*filename):
    with open(path.join(*filename), 'r') as f:
        return f.read()

print(find_packages(exclude=["test*", "test_*", "*_test*"]))

setup(
    name='zaber_motion_bindings_linux',
    version='2.14.0',
    packages=find_packages(exclude=["test*", "test_*", "*_test*"]),
    package_data={
        '': ['*.so']
    },
    description='Linux bindings for Zaber Motion Library',
    long_description='Linux bindings for Zaber Motion Library',
    url='https://gitlab.com/ZaberTech/zaber-motion-lib',
    author='Zaber Technologies Inc.',
    author_email='contact@zaber.com',
    license='MIT',

    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Libraries',
    ],
    keywords='',
    install_requires=[],
    extras_require={'build':['invoke']}
)
