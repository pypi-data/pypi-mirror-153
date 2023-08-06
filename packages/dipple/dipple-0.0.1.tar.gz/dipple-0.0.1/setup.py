from setuptools import setup

# For long description
with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='dipple',
    version='0.0.1',
    description='All of the neural network architecture, with a simple implementation',
    packages =['dipple'],
    license='MIT',
    extras_require={
        "dev": [
            "pytest >= 3.7",
            "check-manifest",
            "twine"
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ],
    python_requires='>=3.7',
    install_requires = ['numpy==1.21.6',
                        'pandas==1.3.5',
                        'matplotlib==3.2.2'],
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Saran Pannasuriyaporn",
    author_email="runpan4work@gmail.com",
    url="https://github.com/wallik2/dipple"
)