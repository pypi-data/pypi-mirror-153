# pip install setuptools

import setuptools

with open("README.MD", "r") as file:
    long_description = file.read() 


setuptools.setup(
    name="python_lesson_15",
    version="0.0.1",
    author="Daniil Kimstach",
    author_email="daniilkimstachp@gmail.com",
    description="Package for test",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
  "Programming Language :: Python :: 3.8",
  "License :: OSI Approved :: MIT License",
  "Operating System :: OS Independent",
 ],
    python_requires='>=3.6'
)


