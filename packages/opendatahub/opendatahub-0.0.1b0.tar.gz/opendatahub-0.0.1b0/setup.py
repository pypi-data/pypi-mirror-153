import os
import setuptools

about = {}
here = os.path.abspath(os.path.dirname(__file__))
with open(
    os.path.join(here, "opendatahub", "__version__.py"), "r", encoding="utf-8"
) as f:
    exec(f.read(), about)

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name=about["__name__"],
    version=about["__version__"],
    author="Wang Rui",
    author_email="wangrui@pjlab.org.cn",
    description="Python SDK for explore opendatahub datasets.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.shlab.tech/dps/opendatalab-python-sdk/-/tree/dev-datahub",
    project_urls={
        "Bug Tracker": "https://gitlab.shlab.tech/dps/opendatalab-python-sdk/-/tree/dev-datahub/-/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=["opendatahub"],
    python_requires=">=3.6",
    install_requires=["requests", "oss2", "Click", "tqdm"],
)
