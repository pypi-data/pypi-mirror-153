import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

__version__ = "0.8.4"

setuptools.setup(
    name="badges-gitlab",
    version=__version__,
    author="Felipe P. Silva",
    author_email="felipefoz@gmail.com",
    description="Generate badges for Gitlab Projects in Public and Private Repositories",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT License",
    url="https://gitlab.com/felipe_public/badges-gitlab",
    project_urls={
        "Bug Tracker": "https://gitlab.com/felipe_public/badges-gitlab/-/issues",
        "Documentation": "https://badges-gitlab.readthedocs.io",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.8",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers"
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    install_requires=['anybadge', 'iso8601', 'python-gitlab', 'junitparser', 'toml', 'requests', 'xmltodict'],
    entry_points={
        'console_scripts': ['badges-gitlab=badges_gitlab.cli:main']
    },
    python_requires=">=3.8",
)
