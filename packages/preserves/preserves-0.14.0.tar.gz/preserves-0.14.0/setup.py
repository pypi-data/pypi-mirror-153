from setuptools import setup

setup(
    name="preserves",
    version="0.14.0",
    author="Tony Garnock-Jones",
    author_email="tonyg@leastfixedpoint.com",
    license="Apache Software License",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
    ],
    packages=["preserves"],
    url="https://gitlab.com/preserves/preserves",
    description="Experimental data serialization format",
    install_requires=[],
    python_requires=">=3.6, <4",
    setup_requires=['setuptools_scm'],
    include_package_data=True,
)
