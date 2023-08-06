from setuptools import setup, find_packages

from pathlib import Path

__version__ = ""
line = open(Path(__file__).parent / f"utilitys/__version__.py").readline()
exec(line)

here = Path(__file__).parent


def getRequirements():
    lines = (here / "requirements.txt").open("r").readlines()
    required = []

    for line in lines:
        if not line.startswith("#"):
            required.append(line.strip("\n"))
    return required


# Get the long description from the README file
if (here / "README.md").exists():
    long_description = (here / "README.md").read_text(encoding="utf-8")
else:
    long_description = ""

INSTALL_REQUIRES = getRequirements()
if __name__ == "__main__":
    setup(
        name="utilitys",
        version=__version__,
        package_dir={"utilitys": "utilitys"},
        packages=find_packages(),
        install_requires=INSTALL_REQUIRES,
        extras_require={"full": ["PyQt5>=5.13.0"]},
        include_package_data=True,
        url="https://gitlab.com/ntjess/utilitys",
        download_url="https://gitlab.com/ntjess/utilitys",
        license="MIT",
        description="Potpourri of functionalities",
        long_description=long_description,
        long_description_content_type="text/markdown",
        author="Nathan Jessurun",
        author_email="njessurun@ufl.edu",
        classifiers=[
            "Development Status :: 3 - Alpha",  # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
            "Intended Audience :: Developers",  # Define that your audience are developers
            "Topic :: Software Development :: Build Tools",
            "License :: OSI Approved :: MIT License",  # Again, pick a license
            "Programming Language :: Python :: 3",  # Specify which python versions that you want to support
        ],
        python_requires=">=3.7.*",
    )
