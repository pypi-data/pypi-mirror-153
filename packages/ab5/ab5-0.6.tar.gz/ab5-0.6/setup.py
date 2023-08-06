from setuptools import setup, find_packages



setup(
    name='ab5',
    version='0.6',
    author="Ab.5#3363",
    description="print ascii art with gratient colors",
    long_description_content_type="text/markdown",
    long_description=open("README.md", encoding="utf-8").read(),
    url = "https://github.com/xxa2005/",
    keywords=['color', 'python', 'colors', 'cool', 'gratient', 'fade', 'shadow'],
    packages=["ab5"],
    classifiers=[
      "Intended Audience :: Developers",
      "Programming Language :: Python :: 3",
      "License :: OSI Approved :: MIT License",
      "Operating System :: OS Independent",
    ]
)