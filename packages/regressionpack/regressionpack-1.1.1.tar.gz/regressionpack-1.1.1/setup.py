from setuptools import setup, find_packages

def readme():
    with open('README.md') as f:
        return f.read()

setup(
    name="regressionpack",
    version="1.1.1",
    author="FusedSilica",
    author_email="caronmartin3@gmail.com",
    description="Library for making regression with errorbars a walk in the park. ",
    long_description=readme(),
    long_description_content_type = 'text/markdown',
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Education",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.7",
        "Topic :: Scientific/Engineering :: Mathematics",
    ],
    url="https://pypi.org/project/regressionpack/",
    packages=find_packages(),
    python_requires=">=3.8.3",
    install_requires = [
        "numpy>=1.21.5",
        "scipy>=1.7.3",
        "matplotlib>=3.1",
        ],
    include_package_data=True,
    zip_safe=False,
)
