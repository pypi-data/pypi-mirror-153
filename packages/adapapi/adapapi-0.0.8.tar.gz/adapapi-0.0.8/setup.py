from setuptools import setup, find_packages

from pathlib import Path
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text()

setup(
    name='adapapi',
    version='0.0.8',
    description='A simple Python package using Appen API',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='appenps',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    packages=find_packages(),
    python_requires='>=3.6, <4',
    install_requires=['requests', 'pandas', 'glog']
)
