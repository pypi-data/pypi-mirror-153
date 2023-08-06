from setuptools import setup, find_packages

from openfile import __version__

setup(
    name="pyopenfile",
    version=__version__,
    author="greene",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "uvicorn",
        "fastapi",
        "pydantic",
        "aiofiles",
        "python-dotenv",
        "requests",
        "click",
    ],
    entry_points={"console_scripts": ["openfile=openfile.__main__:main"]},
)
