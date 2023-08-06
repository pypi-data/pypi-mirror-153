import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="redflagbpm",
    version="0.0.2",
    author="Germán Dressino",
    author_email="gdressino@redflag.dev",
    description="BPM service extension",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/redflagdev/redflagbpm-python",
    project_urls={
        "Bug Tracker": "https://gitlab.com/redflagdev/redflagbpm-python/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.8",
    install_requires=['vertx-eventbus-client']
)
