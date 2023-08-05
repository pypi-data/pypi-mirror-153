from setuptools import setup, find_packages

with open('README.md') as f:
    long_description = f.read()

setup(
    name='otree-qvsr',
    version='0.2',
    description='QVSR package',
    long_description_content_type='text/markdown',
    long_description=long_description,
    author='Joseph Noblepal',
    author_email='josephnoblepal@gmail.com',
    license='MIT',
    packages=find_packages(),
    zip_safe=False,
    install_requires=[],  # add any additional packages that
    # needs to be installed along with your package. Eg: 'caer'
    keywords=['python', 'qvsr', 'otree'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: Unix",
    ]
)
