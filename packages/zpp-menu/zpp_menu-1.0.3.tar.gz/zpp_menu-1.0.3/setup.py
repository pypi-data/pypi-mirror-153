from setuptools import setup
import os
import zpp_menu

setup(name="zpp_menu",
      version=zpp_menu.__version__,
      author="ZephyrOff",
      author_email="contact@apajak.fr",
      keywords = "menu terminal zephyroff",
      classifiers = ["Development Status :: 5 - Production/Stable", "Environment :: Console", "License :: OSI Approved :: MIT License", "Programming Language :: Python :: 3"],
      packages=["zpp_menu"],
      description="Générateur d'un menu à touches fléchées",
      long_description = open(os.path.join(os.path.dirname(__file__), 'README.md')).read(),
      long_description_content_type='text/markdown',
      url = "https://github.com/ZephyrOff/py-zpp_menu",
      platforms = "ALL",
      license="MIT")