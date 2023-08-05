import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bullycomp",
    version="0.0.1",
    author="daichi kitazawa",
    author_email="s2022008@stu.musashino-u.ac.jp",
    description="A package compares the number of bullying incidents each year",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/DaichiKitazawa/bully",
    project_urls={
        "Bug Tracker": "https://github.com/DaichiKitazawa/bully",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"bullycomp": "src"},
    py_modules=['bullycomp'],
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.7",
    entry_points = {
        'console_scripts': [
            'bullycomp = bullycomp:main'
        ]
    },
)
