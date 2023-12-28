from setuptools import setup, find_packages

with open('requirements.txt', 'r') as file_handler:
    requirements = file_handler.readlines()

setup(
    name='dollop',
    version='1.0.0',
    author='Michael Peter Dunne',
    include_package_data=True,
    install_requires=requirements,
    packages=find_packages(include=['dollop', 'dollop.*']),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
    ],
)
