import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="medicalworkers",
    version="0.0.6",
    author="kanako akamine",
    author_email="s2022068@stu.musashino-u.ac.jp",
    description="A package for visualizing medical workers of up to 4 countries",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kanako68/medicalworkers",
    project_urls={
        "Bug Tracker": "https://github.com/kanako68/medicalworkers",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    py_modules=['medicalworkers'],
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.8",
    entry_points = {
        'console_scripts': [
            'medicalworkers = medicalworkers:main'
        ]
    },
)
