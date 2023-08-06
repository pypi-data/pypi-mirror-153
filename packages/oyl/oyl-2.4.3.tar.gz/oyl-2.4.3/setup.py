from setuptools import setup,find_packages
setup(name='oyl',version='2.4.3',author='Lin Ouyang', 
    packages=["oyl","oyl.nn"], 
    include_package_data=True,
    install_requires=["numpy","matplotlib","cartopy","pandas",
                      "xarray","sklearn","pyshp"]
)
