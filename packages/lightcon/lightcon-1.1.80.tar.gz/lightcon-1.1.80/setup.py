# -*- coding: utf-8 -*-
'''
Created on Wed Feb  5 16:19:16 2020

@author: butkus
'''
import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

with open('../latest_version.txt', 'r') as f:
    content = f.read()
    version_major, version_minor, version_revision = content.split('.')        

version_revision = int(version_revision) + 1;
new_version_string = '{:}.{:}.{:}'.format(version_major, version_minor, version_revision)

with open('../latest_version.txt', 'w') as f:
    f.write(new_version_string)
    
setuptools.setup(
    name='lightcon', # Replace with your own username
    version=new_version_string,
    author='Vytautas Butkus',
    author_email='vytautas.butkus@lightcon.com',
    description='A set of APIs to Light Conversion devices',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://bitbucket.org/harpiasoftware/light-conversion-apis.git',
    install_requires = ['pythonnet>=2.5.0tcon', 'pyserial', 'numpy', 'matplotlib', 'requests'],
    packages=setuptools.find_packages(),
    data_files = [('Lib/site-packages/lightcon/harpia_daq', 
                   ['lightcon/harpia_daq/LightConversion.Hardware.HarpiaDaq.dll', 
                    'lightcon/harpia_daq/FTD2XX_NET.dll', 
                    'lightcon/harpia_daq/LightConversion.Abstractions.dll',
                    'lightcon/harpia_daq/System.Threading.dll']),
                ('Lib/site-packages/lightcon/fast_daq', 
                   ['lightcon/fast_daq/LightConversion.Hardware.FastDaq.dll', 
                    'lightcon/fast_daq/FTD2XX_NET.dll', 
                    'lightcon/fast_daq/LightConversion.Abstractions.dll',
                    'lightcon/fast_daq/System.Threading.dll']),
                ('Lib/site-packages/lightcon/common', 
                   ['lightcon/common/komodo.dll']),
                ('Lib/site-packages/lightcon/style', 
                   ['lightcon/style/lclogo.png',
                    'lightcon/style/lcstyle.mplstyle'])],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Development Status :: 1 - Planning',
    ],
    project_urls = {
            'Examples': 'https://bitbucket.org/harpiasoftware/light-conversion-apis/src/master/examples/'},
    python_requires='>=3.6',
)

