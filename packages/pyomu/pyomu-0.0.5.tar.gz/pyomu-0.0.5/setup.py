import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

# with open('requirements.txt', 'r') as f:
#     install_requires = f.read().split('\n')[:-1]

setuptools.setup(
     name='pyomu',
     version='0.0.5', 
     author="Sebastián Anapolsky",
     author_email="sanapolsky@gmail.com",
     description="Performs accessibility analysis.",
     long_description=long_description,
     long_description_content_type="text/markdown",
     url="https://github.com/OMU",
     packages=setuptools.find_packages(),
     classifiers=[
         "Programming Language :: Python :: 3",
         "Operating System :: OS Independent",
     ],
     install_requires=['googlemaps', 'tzwhere', 'unidecode', 'osmnx', 'h3', 'mapclassify', 'osmnet'],
     python_requires='>=3.7'
 )
