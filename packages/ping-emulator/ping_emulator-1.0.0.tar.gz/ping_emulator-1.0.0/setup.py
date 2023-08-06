#!/usr/bin/env python3

from setuptools import setup, find_packages


setup(name='ping_emulator',
      version='1.0.0',
      python_requires='>=3.4',
      description='Python library to emulate Ping devices',
      long_description='Python library to emulate Ping devices',
      long_description_content_type='text/markdown',
      author='Alexis Fetet',
      author_email='alexis.fetet@outlook.com',
      url='https://github.com/AlexisFetet/Ping360_emulator',
      packages=find_packages(), install_requires=['pyserial', 'future','bluerobotics-ping'],
      classifiers=[
          "Programming Language :: Python",
          "License :: OSI Approved :: MIT License",
          "Operating System :: OS Independent",
      ],
      scripts=['ping_emulator/emulated_ping360.py'
               ]
      )