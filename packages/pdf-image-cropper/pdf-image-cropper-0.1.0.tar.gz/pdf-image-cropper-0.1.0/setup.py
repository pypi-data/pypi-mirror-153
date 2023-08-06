from setuptools import find_packages, setup
import os

from pdfcropper import __version__, __author__, __email__, __url__, __pypi_deps__

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

setup(
    name='pdf-image-cropper',
    version=__version__,
    description='Crop pdf and conver to png',
    long_description=read('README.md'),
    long_description_content_type='text/markdown',
    keywords='pdf crop png',
    author=__author__,
    author_email=__email__,
    url=__url__,
    license='MIT',
    platforms='POSIX',
    python_requires='>=3.7',
    packages=find_packages(),
    install_requires=__pypi_deps__,
    classifiers=[
        'Development Status :: 1 - Planning',
        'Intended Audience :: Science/Research',
        'Environment :: Console',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3.7',
    ],
    entry_points = {
        'console_scripts': ['pdfcropper=pdfcropper.command_line:main'],
    }
)
