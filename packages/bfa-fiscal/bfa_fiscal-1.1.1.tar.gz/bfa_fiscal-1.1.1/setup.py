from distutils.core import setup
from setuptools import setup

setup (
    name = 'bfa_fiscal',        
    packages = ['bfa_fiscal'],  
    version = '1.1.1',      
    license='GPLv3',       
    description = 'Paquete de conectividad con los servicios web de AFIP',  
    author = 'German Basisty',                 
    author_email = 'german.basisty@basisty.com',     
    url = 'http://www.basisty.com',
    keywords = ['afip', 'Fiscal'],  
    install_requires=[     
        'zeep'
    ],
  classifiers=[
    'Development Status :: 5 - Production/Stable',    
    'Intended Audience :: Developers',      
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
  ],
)