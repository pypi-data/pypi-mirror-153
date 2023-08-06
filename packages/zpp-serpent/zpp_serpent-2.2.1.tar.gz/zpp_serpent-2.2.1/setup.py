from setuptools import setup
import os
import zpp_serpent

setup(name="zpp_serpent",
      version=zpp_serpent.__version__,
      author="ZephyrOff",
      author_email="contact@apajak.fr",
      keywords = "cipher chiffrement serpent zephyroff",
      classifiers = ["Development Status :: 5 - Production/Stable", "Environment :: Console", "License :: OSI Approved :: MIT License", "Programming Language :: Python :: 3"],
      packages=["zpp_serpent"],
      description="Implémentation de l'algorithme de chiffrement Serpent en python3",
      long_description = open(os.path.join(os.path.dirname(__file__), 'README.md')).read(),
      long_description_content_type='text/markdown',
      url = "https://github.com/ZephyrOff/py-zpp_serpent",
      platforms = "ALL",
      license="MIT")