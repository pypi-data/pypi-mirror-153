from setuptools import find_packages
from setuptools import setup

setup(
    name="reddit-decider",
    description="Reddit's python experiments framework",
    long_description="Reddit's Python experiments framework. Bucketing, targeting, overrides, and dynamic config logic is implementated in Rust and wrapped in this Python package.",
    long_description_content_type="text/markdown",
    url="https://github.snooguts.net/reddit/decider-py",
    project_urls={
        "Documentation": "https://reddit-experiments.readthedocs.io/",
    },
    author="matt knox",
    author_email="matt.knox@reddit.com",
    license="MIT",
    use_scm_version=True,
    packages=find_packages(),
    python_requires=">=3.7",
    setup_requires=["setuptools_scm"],
    install_requires=["reddit-edgecontext>=1.0.0a3,<2.0", "maturin>=0.10,<0.13"],
    package_data={"reddit_experiments": ["py.typed"]},
    zip_safe=True,
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Topic :: Software Development :: Libraries",
    ],
)
