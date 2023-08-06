from setuptools import setup
import os
import zpp_color

setup(name="zpp_color",
      version=zpp_color.__version__,
      author="ZephyrOff",
      author_email="contact@apajak.fr",
      keywords = "color terminal zephyroff",
      classifiers = ["Development Status :: 5 - Production/Stable", "Environment :: Console", "License :: OSI Approved :: MIT License", "Programming Language :: Python :: 3"],
      packages=["zpp_color"],
      description="Colorisation de texte dans un terminal",
      long_description = open(os.path.join(os.path.dirname(__file__), 'README.md')).read(),
      long_description_content_type='text/markdown',
      url = "https://github.com/ZephyrOff/py-zpp_color",
      platforms = "ALL",
      license="MIT")