import setuptools

# Reads the content of your README.md into a variable to be used in the setup below
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name='pedomodels',                           # should match the package folder
    packages=['pedomodels'],                     # should match the package folder
    version='0.0.3',                                # important for updates
    license='MIT',                                  # should match your chosen license
    description='Testing installation of Package',
    long_description=long_description,              # loads your README.md
    long_description_content_type="text/markdown",  # README.md is of type 'markdown'
    author='Gaston Mendoza',
    author_email='mendoveirana@gmail.com',
    url='https://github.ugent.be/gmendoza/pedomodels', 
    project_urls = {                                # Optional
        "Bug Tracker": "https://github.ugent.be/gmendoza/pedomodels/issues"
    },
    install_requires=['requests'],                  # list all packages that your package uses
    keywords=["pypi", "pedomodels", "tutorial"], #descriptive meta-data
    classifiers=[                                   # https://pypi.org/classifiers
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Documentation',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
    ],
    
    download_url="https://github.ugent.be/gmendoza/pedomodels.git",
)