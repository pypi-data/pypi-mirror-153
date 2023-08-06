from setuptools import setup
import os
 
setup(
    name='exoplasim',
    version='3.1.2',
    packages=['exoplasim',],
    zip_safe=False,
    install_requires=["numpy>=1.16","matplotlib","scipy"],
    extras_require = {"netCDF4": ["netCDF4"],
                      "HDF5": ["h5py"],
                      "petitRADTRANS": ["petitRADTRANS"]},
    include_package_data=True,
    author='Adiv Paradise',
    author_email='paradise.astro@gmail.com',
    license='GNU General Public License',
    license_files=["LICENSE.TXT",],
    url='https://github.com/alphaparrot/ExoPlaSim',
    description='Exoplanet GCM',
    long_description_content_type='text/x-rst',
    long_description=open('README.rst').read(),
    )
