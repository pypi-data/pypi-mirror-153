from setuptools import setup
from setuptools import find_packages


requires = ["cryptography >= 37.0.2"]


setup(
    name='symbol-hkdf-python',
    version='0.2.1',
    description='encrypt and decrypt tool for symbol',
    url='https://github.com/monakaJP/symbol-hkdf-python',
    author='monakaJP',
    author_email='notify.monakaxym@gmail.com',
    license='apache2.0',
    keywords='https://github.com/monakaJP/symbol-hkdf-python',
    packages=find_packages("src"),
    package_dir={"": "src"},
    install_requires=requires,
    classifiers=[
        'Programming Language :: Python :: 3.6',
    ],
)