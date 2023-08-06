import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="arcanum-newspaper-segmentation-client",
    version="1.4.1",
    author="Biszak Előd (Arcanum Ltd)",
    author_email="elod.biszak@arcanum.com",
    description="Client for Arcanum's Newspaper Segmentation API",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.arcanum.com/en/newspaper-segmentation/",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'pillow',
        'boto3',
        'requests',
        'numpy'
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
