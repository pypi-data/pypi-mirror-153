from setuptools import setup

# read the contents of your README file
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(name = 'epmwebapi', 
      version = '1.8.37', 
      author = 'Elipse Software Ltda', 
      packages = ['epmwebapi'], 
      include_package_data=True,
      description = '', 
      long_description = long_description, 
      long_description_content_type='text/markdown',
      url = 'https://github.com/elipsesoftware/epmwebapi',
      python_requires='>=3.6, <4',
      install_requires=[
          'numpy',
          'requests',
          'python-dateutil',
          'pytz',
          'pythonnet',
      ],
      data_files = [("", ["LICENSE.txt"]),("", ["Readme.md"]),("dll_references", ["epmwebapi/dll_references/Elipse.Epm.AddressSpaceModel.dll"]),("dll_references", ["epmwebapi/dll_references/EpmData.dll"])],
      classifiers=[
      'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
      'Intended Audience :: Developers',      # Define that your audience are developers
      'Topic :: Software Development :: Build Tools',
      'License :: OSI Approved :: MIT License',   # Again, pick a license
      'Programming Language :: Python :: 3.6',
      'Programming Language :: Python :: 3.7',],)

