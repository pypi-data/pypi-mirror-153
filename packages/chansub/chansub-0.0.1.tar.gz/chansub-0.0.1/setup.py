import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="chansub",
    version="0.0.1",
    author="ayaka wada",
    author_email="s2022040@stu.musashino-u.ac.jp",
    description="Number of channel subscribersNumber of channel subscribers",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ayaka-wada/chansub",
    project_urls={
        "Bug Tracker": "https://github.com/ayaka-wada/chansub",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    py_modules=['chansub'],
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.8",
    entry_points = {
        'console_scripts': [
            'chansub = chansub:main'
        ]
    },
)
