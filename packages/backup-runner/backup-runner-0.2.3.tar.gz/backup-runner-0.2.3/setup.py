from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

module_name = "backuprunner"
project_slug = "backup-runner"

setup(
    name=project_slug,
    use_scm_version=True,
    url="https://github.com/Senth/backup-runner",
    license="MIT",
    author="Matteus Magnusson",
    author_email="senth.wallace@gmail.com",
    description="Run a backup script on your local server",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=[module_name],
    entry_points={"console_scripts": [f"{project_slug}={module_name}.__main__:main"]},
    include_package_data=True,
    data_files=[(f"config", [f"config/{project_slug}-example.cfg"])],
    install_requires=[
        "psutil",
        "tealprint",
        "blulib",
    ],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "License :: OSI Approved :: MIT License",
        "Environment :: Console",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
    ],
    setup_requires=["setuptools_scm"],
    python_requires=">=3.8",
)
