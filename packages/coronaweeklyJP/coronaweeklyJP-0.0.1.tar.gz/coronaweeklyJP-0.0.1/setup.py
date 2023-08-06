import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="coronaweeklyJP",
    version="0.0.1",
    author="suzuto kirishima",
    author_email="kiri.suzuto@gmail.com",
    description='A package displays rate of increase in corona patients in Japanese prefectures.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/SuzutoKirishima/corona-weekly-JP",
    project_urls={
        "Bug Tracker": "https://github.com/SuzutoKirishima/corona-weekly-JP",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    py_modules=['coronaweeklyJP'],
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.7",
    entry_points = {
        'console_scripts': [
            'coronaweeklyJP = coronaweeklyJP:main'
        ]
    },
)