import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='tradedoubler_api_client',
    version='0.7.2',
    description='Unofficial simple python wrapper for Tradedoubler API',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='https://github.com/adamczarnecki/tradedoubler_api_client',
    author='Adam Czarnecki',
    author_email='adam@czarnecki.cz',
    license='MIT',
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
    py_modules=['tradedoubler_api_client'],
    package_dir={'': 'src'},
    install_requires=[
        'requests'
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent'
    ],
    zip_safe=False)
