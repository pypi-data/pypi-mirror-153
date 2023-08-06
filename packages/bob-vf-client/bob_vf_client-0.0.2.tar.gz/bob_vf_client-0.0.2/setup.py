# python setup.py sdist

import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bob_vf_client",
    version="0.0.2",
    author="Roberto Alonso Gomez",
    author_email="rag700504@hotmail.com",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.voxelfarm.com/help/PythonCookbook.html",
    project_urls={
        "Bug Tracker": "https://github.com/voxelfarm/voxelfarmclient/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    install_requires = [
    ],
    extras_require = {
        "dev": [
            "pytest>=3.7",
        ],
    }
)