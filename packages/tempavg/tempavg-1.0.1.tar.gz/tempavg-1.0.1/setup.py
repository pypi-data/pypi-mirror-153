import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tempavg",
    version="1.0.1",
    author="yumiko shimpo",
    author_email="yumikoshippo@gmail.com",
    description="Changes in average temperature in Japanese cities",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Shimpo-Yumiko/",
    project_urls={
        "Bug Tracker": "https://github.com/Shimpo-Yumiko/",
    },
    classifiers=[
        "Programming Language :: Python :: 3"
    ],
    package_dir={"": "src"},
    py_modules=['tempavg'],
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.7",
    entry_points = {
        'console_scripts': [
            'tempavg = tempavg:main'
        ]
    },
)
