from setuptools import setup, find_namespace_packages


def _read(filename: str) -> str:
    """
    Reads in the content of the file.

    :param filename:    The file to read.
    :return:            The file content.
    """
    with open(filename, "r") as file:
        return file.read()


setup(
    name="wai.annotations.grayscale",
    description="Grayscale image segmentation format plugins for wai.annotations.",
    long_description=f"{_read('DESCRIPTION.rst')}\n"
                     f"{_read('CHANGES.rst')}",
    url="https://github.com/waikato-datamining/wai-annotations-grayscale",
    classifiers=[
        'Development Status :: 4 - Beta',
        'License :: OSI Approved :: Apache Software License',
        'Topic :: Scientific/Engineering :: Mathematics',
        'Programming Language :: Python :: 3',
    ],
    license='Apache License Version 2.0',
    package_dir={
        '': 'src'
    },
    packages=find_namespace_packages(where='src'),
    namespace_packages=[
        "wai",
        "wai.annotations"
    ],
    version="1.0.0",
    author='Corey Sterling',
    author_email='coreytsterling@gmail.com',
    install_requires=[
        "wai.annotations.core>=0.1.6"
    ],
    entry_points={
        "wai.annotations.plugins": [
            # Image Segmentation Formats
            "from-grayscale-is=wai.annotations.grayscale.specifier:GrayscaleInputFormatSpecifier",
            "to-grayscale-is=wai.annotations.grayscale.specifier:GrayscaleOutputFormatSpecifier",
        ]
    }
)
