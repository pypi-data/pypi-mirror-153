import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="typhooninfo",
    version="0.0.3",
    author="yugo ishihara",
    author_email="s2022041@stu.musashino-u.ac.jp",
    description="A package for visualization about typhoon in Japan",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yugo-Ishihara/typhooninfo",
    project_urls={
        "typhooninfo": "https://github.com/yugo-Ishihara/typhooninfo",
    },
    classifiers=[
        "Programming Language :: Python :: 3.9",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    py_modules=['typhooninfo'],
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.9",
    entry_points = {
        'console_scripts': [
            'typhooninfo = typhooninfo:main'
        ]
    },
)
