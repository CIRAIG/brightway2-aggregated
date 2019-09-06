import setuptools

with open("README.rst", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='bw2agg',
    version='0.1',
    author="Pascal Lesage",
    author_email="pascal.lesage@polymtl.ca",
    description="Extension to brightway2 package to create and work with aggregated data",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/pascallesage/brightway2-aggregated",
    install_requires=[
        'bw2calc',
        'bw2data',
        'numpy',
    ],
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3.7",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Scientific/Engineering :: Mathematics',
    ],
)