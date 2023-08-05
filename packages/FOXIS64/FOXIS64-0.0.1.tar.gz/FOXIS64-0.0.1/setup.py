import setuptools

with open("README.md", "r") as fh:
	long_description = fh.read()

setuptools.setup(

	name="FOXIS64",

	version="0.0.1",

	author="Ann",

	author_email="Anyasutiko6403938@gmail.com",

	description="For users",
	
	long_description=long_description,

	long_description_content_type="text/markdown",
	
	url="",

	packages=setuptools.find_packages(),
	
	classifiers=[
		"Programming Language :: Python :: 3.6",
		"License :: OSI Approved :: MIT License",
		"Operating System :: OS Independent",
	],
    
	python_requires='>=3.8',
)