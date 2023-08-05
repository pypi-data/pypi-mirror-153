import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="encn",
    version="0.0.1",
    author="reo nishizawa",
    author_email="s2022054@stu.musashino-u.ac.jp",
    description="A package for energy cosumption",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ytakefuji/score-covid-19-policy",
    project_urls={
        "Bug Tracker": "https://github.com/Leo-Urata/energy-consumption",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    py_modules=['encn'],
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    entry_points = {
        'console_scripts': [
            'encn = encn:main'
        ]
    },
)
