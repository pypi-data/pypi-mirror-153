import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="JoyCat",
    version="0.0.1",
    author="yuta ishii",
    author_email="s2022052@stu.musashino-u.ac.jp",
    description = 'This package visualizes the happiness of cats based on Japanese traditional lore.',
    long_description='In Japan, there is a saying, "When the autumn rains fall, the cat\'s face becomes three feet long. This means that the cat\'s face is longer and more joyful on rainy days than on sunny days in autumn, because the temperature is higher on rainy days. We assume that the more it rains, the more pleased the cat will be. Of course, this is limited to autumn. If it is autumn now, this will help. There is a lot going on in the world right now. But it does not matter to cats. If cats are happy, the world will be peaceful.',
    long_description_content_type="text/markdown",
    url="https://github.com/yuta08/CatJoy",
    project_urls={
        "Bug Tracker": "https://github.com/yuta08/CatJoy",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    py_modules=['kotonohagetter'],
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.7",
    entry_points = {
        'console_scripts': [
            'CatJoy = CatJoy:main'
        ]
    },
)