import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="vrsjp",
    version="0.0.1",
    author="Iku Sekido",
    author_email="s2022021@stu.musashino-u.ac.jp",
    description="A package for scoring number of vaccinated people in Japan",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/sekidoiku/vrsjp",
    project_urls={
        "vrsjp": "https://github.com/sekidoiku/vrsjp",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    py_modules=['vrsjp'],
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    entry_points = {
        'console_scripts': [
            'vrsjp = vrsjp:main'
        ]
    },
)
