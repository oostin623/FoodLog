"""
setup.py
    -allows the foodlog package to be installed via:
     $ python setup.py install
     -or installed for development via:
     $ python setup.py develop

     -once installed, the package can be imported from anywhere on the system
      (as opposed to just when within the same directory)
"""

from setuptools import setup

setup(name='FoodLog',
      version='0.1.0',
      description='Web service backend to my food log application webpage',
      author='Austin Jones',
      author_email='oostin623@gmail.com',
      packages=['foodlog', 'foodlog.resources', 'foodlog.common', 'foodlog.test'],
      zip_safe=False,
      install_requires=["Flask == 0.10.1",
                        "flask_restful == 0.3.4"])
