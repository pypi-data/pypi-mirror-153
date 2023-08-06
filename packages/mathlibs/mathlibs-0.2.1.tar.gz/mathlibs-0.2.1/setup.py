from setuptools import setup, find_packages
 
setup(name='mathlibs',
      version='0.2.1',
      url='https://blagon-team.ml/?p=2633',
      license='MIT',
      author='Sergey Kudinov',
      author_email='info@blagon-team.ml',
      description='math theorem',
      packages=['mathlibs'],
      long_description=open('README.md').read(),
      zip_safe=False)