import io

import setuptools


CLIENT_VERSION = "0.0.2"
PACKAGE_NAME = "anydockerizer"

try:
    with io.open("README.md", encoding="utf-8") as f:
        LONG_DESCRIPTION = f.read()
except FileNotFoundError:
    LONG_DESCRIPTION = ""

REQUIRES = []
with open('requirements.txt') as f:
    for line in f:
        line, _, _ = line.partition('#')
        line = line.strip()
        REQUIRES.append(line)

setuptools.setup(
    name=PACKAGE_NAME,
    version=CLIENT_VERSION,
    license="Proprietary",
    description="Anylearn Python Dockerizer",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    author_email="anylearn@nelbds.org.cn",
    author="Dmagine",
    install_requires=REQUIRES,
    python_requires='>=3.7',
    packages=setuptools.find_packages(),
    classifiers=[
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "License :: Other/Proprietary License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    entry_points = '''
        [console_scripts]
        anyd = anydockerizer.cli:anyd
    ''',
)
