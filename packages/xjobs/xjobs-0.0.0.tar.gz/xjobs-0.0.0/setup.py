from setuptools import setup, find_packages, Extension

#######################################
# Prepare list of compiled extensions #
#######################################

extensions = []


#########
# Setup #
#########

setup(
    name='xjobs',
    version='0.0.0',
    description='Management of jobs on clusters',
    url='https://github.com/xsuite/xjobs',
    packages=find_packages(),
    ext_modules = extensions,
    include_package_data=True,
    install_requires=[
        'numpy>=1.0',
        ]
    )
