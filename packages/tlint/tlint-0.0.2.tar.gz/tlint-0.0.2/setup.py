from importlib.metadata import entry_points
import setuptools


def get_file_content(filename: str):
    with open(filename, 'r', encoding='utf-8') as file:
        return file.read()


setuptools.setup(
    name="tlint",
    description="Linter which behaviour is entirely based on a config file.",
    version="0.0.2",
    packages=setuptools.find_packages(),
    entry_points={
        "console_scripts": [
            "tlint=tlint.__main__:main"
        ]
    },
    long_description=get_file_content("README.md"),
    long_description_content_type='text/markdown',
)
