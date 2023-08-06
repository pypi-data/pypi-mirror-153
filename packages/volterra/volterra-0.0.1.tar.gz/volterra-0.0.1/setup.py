from setuptools import setup, find_packages

with open('requirements.txt') as f:
    requirements = f.readlines()

long_description = 'Volterra is lite web server, primarily created for fast development.'

setup(
    name='volterra',
    version='0.0.1',
    author='Ashish Sahu',
    author_email='spiraldeveloper@gmail.com',
    url='https://github.com/stacknix/volterra',
    description='Package for scap server.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    license='MIT',
    packages=find_packages(),
    entry_points={
        'console_scripts': [
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords='python package volterra',
    install_requires=requirements,
    include_package_data=True,
    zip_safe=False
)
