import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
    name="cpkg",
    version="0.2.16",
    author="xiongtianshuo",
    author_email="Mr_Xiongts@163.com",
    description="A package that creates a package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/seoul2k/cPkg",
    project_urls={
        "Bug Tracker": "https://github.com/seoul2k/cPkg/issues",
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        'Development Status :: 3 - Alpha',
    ],
    packages=['cpkg/'],
    python_requires=">=3",
    install_requires=['shutil'],
    platforms='any',
    options={
        'entry_points': {
            'console_scripts': [
                'createpkg = cpkg.cpkg:main'
            ]
        }
    },
    entry_points={
        'console_scripts': [
            'createpkg = cpkg.cpkg:main'
        ]
    }
)
