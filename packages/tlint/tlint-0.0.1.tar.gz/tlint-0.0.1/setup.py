from importlib.metadata import entry_points
import setuptools

setuptools.setup(
    name="tlint",
    description="Linter which behaviour is entirely based on a config file.",
    version="0.0.1",
    packages=setuptools.find_packages(),
    entry_points={
        "console_scripts": [
            "tlint=tlint.__main__:main"
        ]
    }
)
