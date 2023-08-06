import setuptools

setuptools.setup(
    name='photoencryption',
    packages=setuptools.find_packages(include=['photoEncryption']),
    version='0.0.1',
    description='Encrypting and decrypting messages from images',
    author='Bruno Faliszewski',
    license='MIT',
    install_requires=['pillow', 'numpy'],
)