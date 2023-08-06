import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="steamapex",
    version="1.0.0",
    author="ousyouyou",
    author_email="s2122011@stu.musashino-u.ac.jp",
    description="show Apex on steam",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ousyouyou/steamapex",
    project_urls={
        "Bug Tracker": "https://github.com/ousyouyou/steamapex",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    py_modules=['steamapex'],
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.7",
    entry_points = {
        'console_scripts': [
            'steamapex = steamapex:main'
        ]
    },
)
