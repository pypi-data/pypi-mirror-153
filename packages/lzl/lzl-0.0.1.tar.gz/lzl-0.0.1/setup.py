from time import time
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="lzl",
    version="0.0.1",
    author="Liu Zuo Lin",
    author_email="zlliu246@gmail.com",
    description="A test package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    # url="https://github.com/pypa/sampleproject",
    url="https://github.com/zlliu246/lzl",
    project_urls={
        # "Bug Tracker": "https://github.com/pypa/sampleproject/issues",
        "Bug Tracker": "https://github.com/zlliu246/lzl/issues"
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)

# python3 -m twine upload dist/* -u zlliu --verbose --skip-existing