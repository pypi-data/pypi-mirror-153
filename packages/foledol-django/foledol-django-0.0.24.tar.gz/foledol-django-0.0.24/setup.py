from setuptools import setup, find_packages
setup(
    include_package_data=True,
    package_data={
        # If any package contains *.txt or *.rst files, include them:
        "": ["*.html", "*.rst"],
    }
)