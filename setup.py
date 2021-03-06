from setuptools import setup, find_packages, Extension
import sys
import os
import platform

SRC_DIR = 'src'


def get_version():
    sys.path[:0] = [SRC_DIR]
    return __import__('mogcli').__version__


source_files = ['src/cmogcore/%s.cpp' % s for s in ['cmogcore']]

compile_args = []
if 'SAVE_ATTACK_TABLE' in os.environ.keys():
    compile_args.append('-DSAVE_ATTACK_TABLE')
elif 'LOAD_ATTACK_TABLE' in os.environ.keys():
    compile_args.append('-DLOAD_ATTACK_TABLE')

setup(
    name='mog-cli',
    version=get_version(),
    description='Command Line Interface for Playing Shogi Games',
    author='mogproject',
    author_email='mogproj@gmail.com',
    url='https://github.com/mogproject/mog-cli',
    install_requires=[
    ],
    tests_require=[
    ],
    package_dir={'': SRC_DIR},
    packages=find_packages(SRC_DIR),
    include_package_data=True,
    test_suite='tests',
    entry_points="""
    [console_scripts]
    mog-cli = mogcli.mogcli:main
    """,
    ext_modules=[
        Extension(
            name='cmogcore',
            sources=source_files,
            include_dirs=['/usr/local/include/boost'],
            library_dirs=['/usr/lib', '/usr/local/lib'],
            libraries=['boost_python3'],
            extra_compile_args=['-std=c++1y', '-pthread', '-Wall',
                                '-O3', '-fconstexpr-steps=2147483647'] + compile_args,
            extra_link_args=[],
        )
    ],
)
