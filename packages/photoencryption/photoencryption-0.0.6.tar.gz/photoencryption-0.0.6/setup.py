from setuptools import setup, find_packages

setup(
    name='photoencryption',
    packages=find_packages(include=['photoEncryption', 'photoEncryption.*']),
    version='0.0.6',
    description='Encrypting and decrypting messages from images',
    author='Bruno Faliszewski',
    license='MIT',
    install_requires=['pillow', 'numpy'],
)