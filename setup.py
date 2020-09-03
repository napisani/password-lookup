import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="passwordlookup",
    version="0.0.1",
    author="Nick Pisani",
    author_email="napisani@yahoo.com",
    description="password lookup utility for looking up keepass or bitwarden passwords via a terminal session",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/napisani/password-lookup",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=[
        'colorama==0.4.3',
        'cryptography==3.0',
        'libkeepass==0.2.0',
        'pycparser==2.20',
        'pycrypto==2.6.1',
        'pycryptodomex==3.9.8',
        'pyperclip==1.8.0',
    ]

)
