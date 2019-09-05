import setuptools

setuptools.setup(
     name='bw2agg',
     version='0.1',
     author="Pascal Lesage",
     author_email="pascal.lesage@polymtl.ca",
     description="Extension to brightway2 package to work with aggregated data",
     url="https://gitlab.com/pascal.lesage/brightway2-aggregated",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )