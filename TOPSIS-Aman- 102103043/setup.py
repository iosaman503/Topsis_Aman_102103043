# setup.py

from setuptools import setup, find_packages

setup(
    name='TOPSIS-AMAN-102103043',
    version='0.2',
    packages=find_packages(),
    install_requires=[
        'numpy',
        'pandas',
    ],
    entry_points={
        'console_scripts': [
            'console_scripts = 102103043_script = topsis_aman_102103043.aman:main',

        ],
    },
    author='Aman Verma',
    author_email='averma3_be21@thapar.edu',
    description='A Python package for Topsis analysis',
    long_description="It's a Python Package to implement Topsis by Aman Verma for the first assignment at Thapar University,Patiala",
    license='MIT',
    keywords='topsis analysis',
    url='https://github.com/iosaman503/TOPSIS-AMAN-102103043',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
    ],
)
