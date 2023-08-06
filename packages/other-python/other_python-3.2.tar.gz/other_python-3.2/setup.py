from setuptools import setup,find_packages

with open("README.md", "r", encoding="utf8") as f:
    long_description = f.read()

setup(name='other_python',
      version='3.2',
      description="upgraded version of calc-plus",
      long_description=long_description,
      long_description_content_type="text/markdown",
      url='https://github.com/keegang6705/other-python',
      author='keegang_6705',
      author_email='darunphobwi@gmail.com',
      license='MIT',
      packages=find_packages(),
      install_requires= [''],
      python_requires='>=3.0',
      zip_safe=False)