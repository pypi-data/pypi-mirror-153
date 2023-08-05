import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="wakamaro",
    version="0.0.3",
    author="aiha ikegami",
    author_email="s2022003@stu.musashino-u.ac.jp",
    description="A package for visualizing the number of waka poetry composed by poets in Nijuichidaishu",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/AihaIkegami/wakamaro",
    project_urls={
        "Bug Tracker": "https://github.com/AihaIkegami/wakamaro",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    py_modules=['wakamaro'],
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.8",
    entry_points = {
        'console_scripts': [
            'wakamaro = wakamaro:main'
        ]
    },
)
