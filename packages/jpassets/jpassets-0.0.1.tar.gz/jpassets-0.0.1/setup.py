import setuptools
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
name="jpassets",
version="0.0.1",
author="KosukeYasuhara",
author_email="s2022066@stu.musashino-u.ac.jp",
description="A package for adverse effects on death using VAERS",
long_description=long_description,
long_description_content_type="text/markdown",
url="https://github.com/YasuharaKosuke/jpassets",
project_urls={"Bug Tracker": "https://github.com/YasuharaKosuke/jpassets",},
classifiers=[
"Programming Language :: Python :: 3",
"License :: OSI Approved :: MIT License",
"Operating System :: OS Independent",
],
package_dir={"": "src"},
py_modules=["vaer"],
packages=setuptools.find_packages(where="src"),
python_requires=">=3.8",
entry_points = {'console_scripts':["vaers = vaers:main"]
},
)