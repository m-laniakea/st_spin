from setuptools import setup, find_packages

setup(
      name='st_spin',
      version='0.0.22',
      url='https://github.com/m-laniakea/st_spin',
      license='GPLv1',
      author='eir',
      author_email='m-laniakea@users.noreply.github.com',
      description='Interface for ST SpinFamily motor drivers',
      packages=find_packages(exclude=['tests']),
      long_description=open('README.md').read(),
      long_description_content_type='text/markdown',
      install_requires=[
          'spidev',
          'typing_extensions',
      ],
      zip_safe=False)
