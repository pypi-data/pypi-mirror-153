import setuptools
from distutils.core import setup,Extension

setup(
    name='HalSMPy',
    version='0.0.0.3',
    author="Halwarsing",
    author_email='halolxz@gmail.com',
    description="HalSMCompiler for python",
    ext_modules=[
        Extension(
            'HalSM',
            ['halsm.c',
             'HalSM/HalSM.c'],
            extra_compile_args=['-std=c11','-IHalSM']
        )
    ],
    long_description="HalSMC extension for python",
    packages=['HalSM'],
    package_dir={'HalSM':'HalSM'}
)
