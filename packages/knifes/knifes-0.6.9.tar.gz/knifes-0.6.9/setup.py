import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="knifes",
    version="0.6.9",
    author="knifes",
    author_email="author@example.com",
    description="Swiss Army Knife",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    packages=setuptools.find_packages(),
    python_requires=">=3.0",
    install_requires=[
       # 'cryptography',  # required by aes
       # 'pycrypto',   #  required by aes
       'python-decouple',
       'validators',
       # 'tencentcloud-sdk-python==3.0.600',  #  required by sms
    ]
)
