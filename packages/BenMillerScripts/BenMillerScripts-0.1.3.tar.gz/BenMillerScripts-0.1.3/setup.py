from setuptools import setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
    
setup(
	name='BenMillerScripts',
    url='https://www.gatan.com/resources/python-scripts',
    author='Ben Miller',
    author_email='benmiller002@aol.com',
    packages=['benmillerscripts'],
    # Needed for dependencies
    install_requires=['scikit-learn', 'matplotlib', 'numpy', 'scipy', 'scikit-image', 'pandas', 'tqdm'],
    # *strongly* suggested for sharing
    version='0.1.3',
    # The license can be anything you like
    license='MIT',
    description='Modules for Running Python scripts by Ben Miller in DigitalMicrograph',
    long_description=long_description,
    long_description_content_type="text/markdown",
	python_requires = '>=3.7',
	)