import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()


setuptools.setup(
     name='pjcleanr',  
     version='0.1',
     scripts=['pjcleanr'] ,
     author="Pankaj Jha",
     author_email="mailt@pankajjha.me",
     description="A News Article cleaning package",
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://github.com/pankajjha/pjcleanr",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "License :: OSI Approved :: MIT License",
         "Operating System :: OS Independent",
     ],
 )