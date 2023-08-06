import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="michell-raytracer",
    version="0.0.2",
    author="Viktor Akusov",
    author_email="viktor@akusov.xyz",
    description="Relativistic non-linear raytracer for Schwarzschild's metric.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/viktor-akusov/michell-raytracer",
    project_urls={
        "Bug Tracker": "https://github.com/viktor-akusov/michell-raytracer/issues",
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
        "numpy >= 1.22.4",
        "Pillow >= 9.1.1",
        "progressbar >= 2.5"
    ],
    license = "MIT",
    keywords=["raytracer", "black hole", "nonlinear"],
)
