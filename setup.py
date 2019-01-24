import os
import sys
import shutil

from setuptools import setup
from setuptools import find_packages


def get_readme():
    with open("README.md") as f:
        return f.read()


if sys.argv[-1] == "publish":
    os.system("python setup.py sdist")
    os.system("twine upload dist/*")
    sys.exit()

    shutil.rmtree("dist")
    shutil.rmtree("build")
    shutil.rmtree("luno.egg-info")
    sys.exit()


if sys.argv[-1] == "test":
    print("Running tests only on current environment.")

    os.system("black ./luno")
    os.system("pytest --cov=luno --cov-report=html")
    os.system("rm coverage.svg")
    os.system("coverage-badge -o coverage.svg")
    sys.exit()


if __name__ == "__main__":
    readme = get_readme()

    setup(
        name="luno",
        version="0.3.6",
        description="Luno Crypto Currency Exchanage Python API",
        long_description=readme,
        long_description_content_type="text/markdown",
        author="Bradley Stuart Kirton",
        author_email="bradleykirton@gmail.com",
        url="https://github.com/BradleyKirton/luno",
        packages=find_packages(),
        include_package_data=True,
        license="MIT",
        keywords=["exchange", "crypto currency", "rest", "api", "bitcoin", "etherium"],
        classifiers=[
            "Development Status :: 4 - Beta",
            "Intended Audience :: Developers",
            "Intended Audience :: Financial and Insurance Industry",
            "Operating System :: OS Independent",
            "Topic :: Office/Business :: Financial :: Investment",
            "Topic :: Software Development :: Libraries :: Python Modules",
            "License :: OSI Approved :: MIT License",
            "Programming Language :: Python :: 3 :: Only",
        ],
        install_requires=["requests"],
        extras_require={
            "dev": [
                "treq",
                "pytest_twisted",
                "bumpversion",
                "pytest",
                "pytest-mock",
                "pytest-twisted",
                "coverage-badge",
                "pytest-cov",
                "twine",
            ],
            "async": ["treq"],
        },
    )
