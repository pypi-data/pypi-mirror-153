import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="original.py",
    version="0.0.2",
    author="Yusuke Yamauchi",
    author_email="s2022033@stu.musashino-u.ac.jp",
    description='A package for visualization of aggregate data of players in "original"',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Yusukemaegami/ds-tokuron",
    project_urls={
        "Bug Tracker": "https://github.com/Yusukemaegami/ds-tokuron",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    py_modules=['original'],
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.8",
    entry_points={
        'console_scripts': [
            'original = original:main'
        ]
    },
)
