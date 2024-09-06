from setuptools import setup, find_packages

setup(
    name="docky",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        # List your dependencies here
    ],
    entry_points={
        'console_scripts': [
            'docky=docky.main:main',
        ],
    },
)