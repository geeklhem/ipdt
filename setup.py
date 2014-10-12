from setuptools import setup

setup(name='ipdt',
      version='0.2',
      description='Iterate Prisoner Dilemma Tournament',
      url='http://github.com/geeklhem/ipdt',
      author='Guilhem Doulcier',
      author_email='guilhem.doulcier@ens.fr',
      license='GPLV3',
      packages=['ipdt','ipdt.players'],
      scripts=['bin/ipdt'],
      zip_safe=False)
