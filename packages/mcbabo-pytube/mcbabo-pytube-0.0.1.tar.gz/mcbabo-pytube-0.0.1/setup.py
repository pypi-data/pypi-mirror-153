from setuptools import setup

setup(
    name="mcbabo-pytube",
    version="0.0.1",
    description="Simple Youtube API Wrapper",
    url="https://github.com/mcbabo/pytube",
    py_modules=["pytube"],
    package_dir={"": "mcbabo-pytube"},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    install_requires=[
        "httpx ~= 0.23"
    ]
)
