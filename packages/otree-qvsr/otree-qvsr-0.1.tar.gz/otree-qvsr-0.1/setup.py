from setuptools import setup, find_packages

setup(
    name='otree-qvsr',
    version='0.1',
    description='QVSR package',
    author='Joseph Noblepal',
    author_email='josephnoblepal@gmail.com',
    license='MIT',
    packages=find_packages(),
    zip_safe=False,
    install_requires=[],  # add any additional packages that
    # needs to be installed along with your package. Eg: 'caer'
    keywords=['python', 'qvsr', 'otree'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: Unix",
    ]
)
