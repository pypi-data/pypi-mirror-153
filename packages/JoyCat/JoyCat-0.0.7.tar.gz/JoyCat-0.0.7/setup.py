import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="JoyCat",
    version="0.0.7",
    author="yuta ishii",
    author_email="s2022052@stu.musashino-u.ac.jp",
    description = 'This package visualizes the happiness of cats based on Japanese traditional lore.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yuta08/JoyCat",
    project_urls={
        "Bug Tracker": "https://github.com/yuta08/JoyCat",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    py_modules=['JoyCat'],
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.7",
    entry_points = {
        'console_scripts': [
            'JoyCat = JoyCat:main'
        ]
    },
)
