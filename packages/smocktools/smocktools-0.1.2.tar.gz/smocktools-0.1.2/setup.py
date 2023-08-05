import setuptools

with open("README.md", "r",encoding="utf-8") as fh:
  long_description = fh.read()

setuptools.setup(
  name="smocktools",
  version="0.1.2",
  author="smock",
  author_email="smockg@gmail.com",
  description="A package",
  long_description=long_description,
  long_description_content_type="text/markdown",
  url="https://github.com/smockgithub/smocktools",
  packages=setuptools.find_packages(),
  classifiers=[
  "Programming Language :: Python :: 3",
  "License :: OSI Approved :: MIT License",
  "Operating System :: OS Independent",
  ],
)