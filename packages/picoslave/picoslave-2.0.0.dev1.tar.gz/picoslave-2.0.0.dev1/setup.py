#!/usr/bin/env python3

from pathlib import Path
import shutil

from setuptools import setup

from picoslave import version


def script(name: str, source_path: str) -> str:
    Path(source_path).exists()
    build = Path('build')
    if not build.exists():
        build.mkdir(parents=True, exist_ok=True)
    shutil.copy(source_path, build / name)
    return './' + str(build / name)


setup(
    name='picoslave',
    url='https://gitlab.com/janoskut/picoslave',
    author='Janos Kutscherauer',
    author_email='janoskut@gmail.com',
    license='MIT',
    license_files=['LICENSE'],
    version=version.get(),
    description='PicoSlave is a dual I2C slave simulator for hardware integration testing',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    keywords=['python', 'Raspberry Pi Pico', 'I2C', 'testing', 'mock'],
    platforms=['Linux', 'Raspberry Pi'],
    packages=['picoslave'],
    install_requires=['pyusb>=1.2'],
    python_requires='>=3.7',
    cmdclass={
        'build_py': version.build_py,
        'sdist': version.sdist,
        'install_lib': version.install_lib,
    },
    scripts=[script('picoslave-install', 'util/install.sh')],
    entry_points={
        'console_scripts': [
            'picoslave = picoslave.__main__:main',
        ],
    },
)
