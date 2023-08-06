import setuptools
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()
setuptools.setup(
    name="WaterCountYUse2022",
    version="0.0.1",
    author="Keita Watanabe",
    author_email="s2022038@stu.musashino-u.ac.jp",
    description="Projected water use in 2022",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/KeitaWata/water_analysis",
    project_urls={
        "Bug Tracker": "https://github.com/KeitaWata/water_analysis",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    py_modules=["WaterCountYUse2022"],#
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.8",
    entry_points = {
        "console_scripts": ["WaterCountYUse2022 = WaterCountYUse2022:main"]
    },
)