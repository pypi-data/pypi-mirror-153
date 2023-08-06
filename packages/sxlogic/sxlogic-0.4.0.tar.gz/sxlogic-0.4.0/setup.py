import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sxlogic",
    version="0.4.0",
    author="StreamLogic, LLC",
    description="StreamLogic Python utilities",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    py_modules=["sxlogic"],
    entry_points={
        'console_scripts': [
            'fpgacap = sxlogic.fpgacap:fpgacap',
            'iconvert = sxlogic.iconvert:iconvert',
            'monocle = sxlogic.monocle:moncole',
            ]
        },
    install_requires=['pyserial','numpy','opencv-python']
)
