from setuptools import setup, find_packages

version = '0.1.9'
name = 'slapcache'
long_description = open("README.txt").read() + "\n" + \
    open("CHANGES.txt").read() + "\n"

setup(name=name,
      version=version,
      description="SlapOS Cache Utils",
      long_description=long_description,
      classifiers=[
          "Programming Language :: Python",
      ],
      keywords='slapos shacache',
      license='GPLv3',
      url='http://www.slapos.org',
      author='VIFIB',
      namespace_packages=['slapcache'],
      packages=find_packages(),
      include_package_data=True,
      install_requires=[
          'slapos.libnetworkcache>=0.14.1',
          'iniparse',
          'six',
      ],
      zip_safe=False,
      entry_points={
          'console_scripts': [
              # Those entry points are development version and
              # self updatable API
              'slapcache-upload = slapcache.upload:main',
              'slapcache-conf = slapcache.conf:do_conf',
              'slapcache-download = slapcache.download:main',
          ],
      },
      test_suite="slapcache.test",
)
