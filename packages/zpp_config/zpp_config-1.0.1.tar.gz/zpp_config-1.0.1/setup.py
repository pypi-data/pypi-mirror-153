from setuptools import setup
import os
import zpp_config

setup(name="zpp_config",
      version=zpp_config.__version__,
      author="ZephyrOff",
      author_email="contact@apajak.fr",
      keywords = "config file terminal zephyroff",
      classifiers = ["Development Status :: 5 - Production/Stable", "Environment :: Console", "License :: OSI Approved :: MIT License", "Programming Language :: Python :: 3"],
      packages=["zpp_config"],
      description="Module pour le chargement et la modification de fichier de configuration",
      long_description = open(os.path.join(os.path.dirname(__file__), 'README.md')).read(),
      long_description_content_type='text/markdown',
      url = "https://github.com/ZephyrOff/py-zpp_config",
      platforms = "ALL",
      license="MIT")