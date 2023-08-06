from setuptools import setup, find_packages

setup(
    name='adapapi',
    version='0.0.6',
    description='A simple Python package using Appen API',
    long_description_content_type='text/markdown',
    author='Hayman',
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
