import setuptools
with open("README.md", "r", encoding="utf-8") as fh:
 long_description = fh.read()
setuptools.setup(
name="jpcases",
version="0.0.1",
author="TakumiKousaka",
author_email="s2022013@stu.musashino-u.ac.jp",
description="A package is the number of positive covid-19 in Tokyo, Japan",
long_description=long_description,
long_description_content_type="text/markdown",
url="https://github.com/TakumiKousaka/jpcases",
project_urls={
"jpcases": "https://github.com/TakumiKousaka/jpcases",
},
classifiers=[
"Programming Language :: Python :: 3",
"License :: OSI Approved :: MIT License",
"Operating System :: OS Independent",
],
package_dir={"": "src"},
py_modules=["jpcases"],
packages=setuptools.find_packages(where="src"),
python_requires=">=3.8",
entry_points = {
'console_scripts': [
'jpcases = jpcases:main'
]
},
)
