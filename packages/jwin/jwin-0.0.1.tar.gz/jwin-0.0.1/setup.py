import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="jwin",
    version="0.0.1",
    author="ryosuke yamamoto",
    author_email="ryosukey1724@gmail.com",
    description='A package for visualization of aggregate data of "J League"',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Doraemon-desu/J-league",
    project_urls={
        "Bug Tracker": "https://github.com/Doraemon-desu/J-league",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    py_modules=['J-league'],
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.7",
    entry_points = {
        'console_scripts': [
            'jwin = jwin:main'
        ]
    },
)
