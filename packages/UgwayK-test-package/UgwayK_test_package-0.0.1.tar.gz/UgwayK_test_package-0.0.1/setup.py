import setuptools

with open("README.md", "r") as fh:
    desc = fh.read()
    
setuptools.setup(
    name="UgwayK_test_package", # Replace with your own username
    version="0.0.1",
    author="UgwayK",
    author_email="nuang0530@naver.com",
    description="A small example package",
    long_description=desc,
    long_description_content_type="text/markdown",
    url="https://blog.naver.com/nuang0530",
    packages=setuptools.find_packages(),
    python_requires='>=3.6'
)