from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='phishing_detector',
    packages=find_packages(include=['phishing_detector']),
    version='0.1.1',
    description='Library that questions whether a site is phishing or not',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='ofsenyayla',
    author_email='ofaruksenyyla@gmail.com',
    license='MIT',
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Operating System :: OS Independent"
    ],
    keywords='phishing detection',
    install_requires=['requests', 'validators', 'pandas'],
)
