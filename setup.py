from setuptools import setup, find_packages

setup(
    name="Pizza3",
    version="1.00",
    description="A LAMMPS toolkit",
    author="Olivier Vitrac",
    author_email="olivier.vitrac@agroparistech.fr",
    url="https://github.com/ovitrac/Pizza3",
    packages=find_packages(include=['pizza', 'pizza.*']),
    install_requires=[
        "numpy>=1.21.0"
    ],
    classifiers=[
        "Programming Language :: Python :: 3.10",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.10',
    include_package_data=True,
    zip_safe=True,
)
